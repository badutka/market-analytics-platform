import json
import os
from importlib.resources import files
import streamlit.components.v1 as components

from market_analytics.config.settings import settings


def render_market_widget(
    ticker: str,
    asset_type: str,
    initial_price: float | None,
    previous_close: float | None,
    initial_change: float | None,
    initial_change_pct: float | None,
):

    component_path = files("market_analytics").joinpath(
        "components",
        "market_widget",
    )

    html = component_path.joinpath("index.html").read_text(encoding="utf-8")

    css = component_path.joinpath("style.css").read_text(encoding="utf-8")

    js = component_path.joinpath("webSockets.js").read_text(encoding="utf-8")

    config = json.dumps(
        {
            "ticker": ticker,
            "asset_type": asset_type,
            "initial_price": initial_price,
            "previous_close": previous_close,
            "initial_change": initial_change,
            "initial_change_pct": initial_change_pct,
            "finnhub_key": settings.finnhub_api_key,
        }
    )

    html = html.replace("/* CSS_PLACEHOLDER */", css)
    html = html.replace("/* JS_PLACEHOLDER */", js)
    html = html.replace("CONFIG_PLACEHOLDER", config)

    return components.html(
        html,
        height=250,
        scrolling=False,
    )
