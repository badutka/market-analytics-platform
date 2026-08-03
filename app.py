import streamlit as st
import plotly.express as px
from pathlib import Path

from market_analytics.config.settings import settings
from market_analytics.clients.bigquery import BigQueryClient
from market_analytics.auth.google import get_google_credentials
from market_analytics.config.defaults import FINNHUB_API_URL
from market_analytics.assets.markets import FINNHUB_SYMBOL_MAP, CRYPTO_TICKERS
from market_analytics.config.tables import TARGET_MARTS_TABLE
from market_analytics.clients.http import session

from market_analytics.components.market_card.renderer import render_market_card
from market_analytics.ui.theme import load_theme

st.set_page_config(
    page_title="Market Analytics Terminal",
    layout="wide",
)

load_theme()


st.title("📈 Market Analytics Terminal")
st.caption("Real-time financial analytics dashboard")


def get_finnhub_symbol(ticker):
    return FINNHUB_SYMBOL_MAP.get(ticker, ticker)


def get_asset_type(ticker):
    return "crypto" if ticker in CRYPTO_TICKERS else "stock"


@st.cache_resource
def get_bigquery_client():
    credentials = get_google_credentials(settings)

    return BigQueryClient(
        project_id=settings.gcp_project_id,
        credentials=credentials,
    )


@st.cache_data(ttl=3600)
def load_historical_metrics():
    bq = get_bigquery_client()

    return bq.query_table_dataframe(TARGET_MARTS_TABLE)


def get_market_snapshot(ticker):
    symbol = get_finnhub_symbol(ticker)

    response = session.get(
        FINNHUB_API_URL,
        params={
            "symbol": symbol,
            "token": settings.finnhub_api_key,
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
        "timestamp": int(data["t"]),
    }


try:
    with st.spinner("Loading market analytics..."):
        data = load_historical_metrics()

    available_tickers = data["asset_ticker"].unique().tolist()

    selected_ticker = st.selectbox(
        "Select asset for detailed analysis",
        available_tickers,
    )

    st.divider()

    st.subheader("Live Market Overview")

    dashboard_assets = [
        "AAPL",
        "MSFT",
        "NVDA",
        "BTC-USD",
    ]

    columns = st.columns(4)

    for column, ticker in zip(columns, dashboard_assets):

        with column:
            snapshot = get_market_snapshot(ticker)

            render_market_card(
                ticker=ticker,
                asset_type=get_asset_type(ticker),
                initial_price=snapshot["price"],
                previous_close=snapshot["previous_close"],
                timestamp=snapshot["timestamp"],
                finnhub_key=settings.finnhub_api_key,
            )

    st.divider()

    st.subheader(f"Historical Performance: {selected_ticker}")

    filtered_df = data[data["asset_ticker"] == selected_ticker].sort_values(
        "trading_date"
    )

    fig = px.line(
        filtered_df,
        x="trading_date",
        y=[
            "price_close",
            "moving_avg_14d",
        ],
        labels={
            "value": "Price",
            "trading_date": "Date",
        },
        title=("Closing Price vs " "14-Day Moving Average"),
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#f8fafc"},
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.subheader("Warehouse Records")

    st.dataframe(
        filtered_df,
        use_container_width=True,
    )

except Exception as e:
    st.error(f"Dashboard failed: {e}")
