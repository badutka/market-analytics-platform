import json
from pathlib import Path

import streamlit.components.v1 as components

COMPONENT_PATH = Path(__file__).parent


def mount_market_card(
    ticker,
    asset_type,
    initial_price,
    previous_close,
    timestamp,
    finnhub_key,
):

    html = COMPONENT_PATH.joinpath("index.html").read_text(encoding="utf-8")

    css = COMPONENT_PATH.joinpath("style.css").read_text(encoding="utf-8")

    js = COMPONENT_PATH.joinpath("market_card.js").read_text(encoding="utf-8")

    config = json.dumps(
        {
            "ticker": ticker,
            "asset_type": asset_type,
            "initial_price": initial_price,
            "previous_close": previous_close,
            "timestamp": timestamp,
            "finnhub_key": finnhub_key,
        }
    )

    html = html.replace(
        "/* CSS_PLACEHOLDER */",
        css,
    )

    html = html.replace(
        "/* JS_PLACEHOLDER */",
        js,
    )

    html = html.replace(
        "CONFIG_PLACEHOLDER",
        config,
    )

    html = html.replace(
        "TICKER_PLACEHOLDER",
        ticker,
    )

    return components.html(
        html,
        height=170,
        scrolling=False,
    )
