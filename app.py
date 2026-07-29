import os
import requests

import streamlit as st
import plotly.express as px
from dotenv import load_dotenv
from google.cloud import bigquery

from market_widget import render_market_widget

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp-key.json"

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")

PROJECT_ID = "ms-fin-analytics-dev"
TARGET_MARTS_TABLE = f"{PROJECT_ID}.analytics.fact_asset_performance"

FINNHUB_SYMBOL_MAP = {
    "BTC-USD": "BINANCE:BTCUSDT",
    "ETH-USD": "BINANCE:ETHUSDT",
}

def get_finnhub_symbol(ticker):
    return FINNHUB_SYMBOL_MAP.get(ticker, ticker)

st.set_page_config(page_title="Market Analytics Platform", layout="wide")

st.title("📈 Market Analytics Platform")
st.subheader("Interactive Portfolio Asset Performance Tracking Dashboard")

@st.cache_data(ttl=3600)
def load_historical_metrics():
    client = bigquery.Client(project=PROJECT_ID)

    query = f"""
        SELECT *
        FROM `{TARGET_MARTS_TABLE}`
    """

    return client.query(query).to_dataframe()

def get_asset_type(ticker):
    return "crypto" if ticker in ["BTC-USD", "ETH-USD"] else "stock"


def get_market_snapshot(ticker):
    symbol = get_finnhub_symbol(ticker)

    response = requests.get(
        "https://finnhub.io/api/v1/quote",
        params={
            "symbol": symbol,
            "token": FINNHUB_API_KEY,
        },
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()

    return {
        "price": float(data["c"]),
        "previous_close": float(data["pc"]),
        "change": float(data["d"]),
        "change_pct": float(data["dp"]),
    }

try:
    with st.spinner("Loading validated models from BigQuery warehouse..."):
        data = load_historical_metrics()

    available_tickers = data["asset_ticker"].unique().tolist()

    selected_ticker = st.sidebar.selectbox(
        "🎯 Select Portfolio Asset",
        available_tickers,
    )

    asset_type = get_asset_type(selected_ticker)

    snapshot = get_market_snapshot(selected_ticker)

    st.write(f"### Real-Time Market Widget: {selected_ticker}")

    render_market_widget(
        ticker=selected_ticker,
        asset_type=asset_type,
        initial_price=snapshot["price"],
        previous_close=snapshot["previous_close"],
        initial_change=snapshot["change"],
        initial_change_pct=snapshot["change_pct"],
    )

    filtered_df = (
        data[data["asset_ticker"] == selected_ticker]
        .sort_values("trading_date")
    )

    st.write(f"### Historical Price Trends: {selected_ticker}")

    fig = px.line(
        filtered_df,
        x="trading_date",
        y=["price_close", "moving_avg_14d"],
        labels={
            "value": "Price",
            "trading_date": "Date",
        },
        title="Closing Price vs 14-Day Simple Moving Average",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.write("### Validated Warehouse Records Matrix")
    st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"Dashboard failed: {e}")