import streamlit as st
import plotly.express as px
import logging

from market_analytics.ui.theme import load_theme
from market_analytics.config.settings import settings
from market_analytics.clients.http import session
from market_analytics.auth.google import get_google_credentials
from market_analytics.config.defaults import FINNHUB_API_URL
from market_analytics.assets.markets import (
    FINNHUB_SYMBOL_MAP,
    CRYPTO_TICKERS,
    DASHBOARD_ASSETS,
)
from market_analytics.config.tables import TARGET_MARTS_TABLE
from market_analytics.components.market_feed.mount import mount_market_feed
from market_analytics.components.market_card.mount import mount_market_card
from market_analytics.clients.bigquery import BigQueryClient

logger = logging.getLogger(__name__)

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
def load_price_history():
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

    if response.status_code == 401:
        raise RuntimeError("Finnhub authentication failed")
    response.raise_for_status()

    data = response.json()

    return {
        "price": float(data["c"]),
        "previous_close": float(data["pc"]),
        "change": float(data["d"]),
        "change_pct": float(data["dp"]),
        "timestamp": int(data["t"]),
    }


def market_overview(dashboard_assets):

    for i in range(0, len(dashboard_assets), 4):
        columns = st.columns(4)

        for column, ticker in zip(columns, dashboard_assets[i : i + 4]):
            with column:
                snapshot = get_market_snapshot(ticker)

                mount_market_card(
                    ticker=ticker,
                    asset_type=get_asset_type(ticker),
                    initial_price=snapshot["price"],
                    previous_close=snapshot["previous_close"],
                    timestamp=snapshot["timestamp"],
                    finnhub_key=settings.finnhub_api_key,
                )


def render_market_card(ticker):

    snapshot = get_market_snapshot(ticker)

    mount_market_card(
        ticker=ticker,
        asset_type=get_asset_type(ticker),
        initial_price=snapshot["price"],
        previous_close=snapshot["previous_close"],
        timestamp=snapshot["timestamp"],
        finnhub_key=settings.finnhub_api_key,
    )


@st.fragment
def analysis_panel(data, available_tickers):

    selected_ticker = st.selectbox(
        "Select asset for detailed analysis",
        available_tickers,
    )

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
        width="stretch",
    )

    st.subheader("Warehouse Records")

    st.dataframe(
        filtered_df,
        width="stretch",
    )


try:
    mount_market_feed(settings.finnhub_api_key)

    with st.spinner("Loading market analytics..."):
        data = load_price_history()

    available_tickers = data["asset_ticker"].unique().tolist()

    st.subheader("Live Market Overview")

    market_overview(DASHBOARD_ASSETS)

    st.divider()

    analysis_panel(data, available_tickers)

except Exception:
    logger.exception("Dashboard failed")

    st.error("Dashboard failed to load. Please try again later.")
