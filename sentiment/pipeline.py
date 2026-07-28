from datetime import datetime, timezone
import uuid6

import yfinance as yf

from sentiment.events import extract_events
from sentiment.market import get_market_confirmation
from sentiment.models import MarketIntelligenceResult
from sentiment.sentiment import analyze_events
from sentiment.signal import calculate_signal
from sentiment.news import get_news


def run_pipeline(
    ticker,
    company_name
):

    articles = get_news(ticker)

    extraction = extract_events(
        ticker,
        company_name,
        articles,
    )

    sentiment = analyze_events(
        ticker,
        company_name,
        extraction.events,
    )

    confirmation = get_market_confirmation(
        ticker
    )

    signal = calculate_signal(
        sentiment,
        extraction.events,
        confirmation,
    )

    price = float(
        yf.Ticker(ticker)
        .history(period="1d")
        .Close.iloc[-1]
    )

    return MarketIntelligenceResult(
        analysis_id=str(uuid6.uuid7()),
        ticker=ticker,
        company_name=company_name,
        timestamp=datetime.now(timezone.utc),
        price=price,
        sentiment=sentiment,
        signal=signal,
        market_confirmation=confirmation,
        events=extraction.events,
        articles=articles,
    )