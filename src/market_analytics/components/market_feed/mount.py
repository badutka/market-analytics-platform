import json
from pathlib import Path

import streamlit.components.v1 as components

from market_analytics.assets.markets import CRYPTO_TICKERS, STOCK_TICKERS

COMPONENT_PATH = Path(__file__).parent


def mount_market_feed(api_key):

    html = COMPONENT_PATH.joinpath("index.html").read_text(encoding="utf-8")

    js = COMPONENT_PATH.joinpath("feed.js").read_text(encoding="utf-8")

    config = json.dumps(
        {
            "finnhub_key": api_key,
            "stock_tickers": STOCK_TICKERS,
            "crypto_tickers": CRYPTO_TICKERS,
        }
    )

    html = html.replace(
        "CONFIG_PLACEHOLDER",
        config,
    )

    html = html.replace(
        "/* JS_PLACEHOLDER */",
        js,
    )

    components.html(
        html,
        height=1,
        scrolling=False,
    )
