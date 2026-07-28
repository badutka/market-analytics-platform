import os

import streamlit as st
import plotly.express as px
from dotenv import load_dotenv
from google.cloud import bigquery

from market_widget import render_market_widget

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp-key.json"

PROJECT_ID = "ms-fin-analytics-dev"
TARGET_MARTS_TABLE = f"{PROJECT_ID}.analytics.fact_asset_performance"

st.set_page_config(
    page_title="Market Analytics Platform",
    layout="wide"
)

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
    crypto_assets = [
        "BTC-USD",
        "ETH-USD"
    ]

    return "crypto" if ticker in crypto_assets else "stock"


def get_previous_close(data, ticker):
    asset_df = (
        data[data["asset_ticker"] == ticker]
        .sort_values("trading_date")
    )

    if len(asset_df) < 2:
        return None

    return float(
        asset_df.iloc[-2]["price_close"]
    )


try:
    with st.spinner("Loading validated models from BigQuery warehouse..."):
        data = load_historical_metrics()

    available_tickers = (
        data["asset_ticker"]
        .unique()
        .tolist()
    )

    selected_ticker = st.sidebar.selectbox(
        "🎯 Select Portfolio Asset",
        available_tickers
    )

    asset_type = get_asset_type(
        selected_ticker
    )

    previous_close = get_previous_close(
        data,
        selected_ticker
    )

    st.write(
        f"### Real-Time Market Widget: {selected_ticker}"
    )

    render_market_widget(
        ticker=selected_ticker,
        asset_type=asset_type,
        previous_close=previous_close
    )

    filtered_df = (
        data[data["asset_ticker"] == selected_ticker]
        .sort_values("trading_date")
    )

    st.write(
        f"### Historical Price Trends: {selected_ticker}"
    )

    fig = px.line(
        filtered_df,
        x="trading_date",
        y=[
            "price_close",
            "moving_avg_14d"
        ],
        labels={
            "value": "Price",
            "trading_date": "Date"
        },
        title="Closing Price vs 14-Day Simple Moving Average"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.write(
        "### Validated Warehouse Records Matrix"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

except Exception as e:
    st.error(
        f"Dashboard failed: {e}"
    )