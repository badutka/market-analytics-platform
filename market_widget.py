import json
import os

import streamlit.components.v1 as components
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")


def render_market_widget(ticker: str, asset_type: str, previous_close: float | None):
    component_path = os.path.join(
        os.path.dirname(__file__), "components", "market_widget"
    )

    with open(os.path.join(component_path, "index.html"), "r", encoding="utf-8") as file:
        html = file.read()
    with open(os.path.join(component_path, "style.css"), "r", encoding="utf-8") as file:
        css = file.read()
    with open(os.path.join(component_path, "webSockets.js"), "r", encoding="utf-8") as file:
        js = file.read()

    config = json.dumps(
        {
            "ticker": ticker,
            "asset_type": asset_type,
            "previous_close": previous_close,
            "finnhub_key": FINNHUB_API_KEY,
        },
        ensure_ascii=False,
    )

    html = html.replace("/* CSS_PLACEHOLDER */", css)
    html = html.replace("/* JS_PLACEHOLDER */", js)
    html = html.replace("CONFIG_PLACEHOLDER", config)

    return components.html(html, height=250, scrolling=False)
