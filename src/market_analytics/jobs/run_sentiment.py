from datetime import datetime, timezone
import uuid6
import logging
import yfinance as yf

from market_analytics.sentiment.events import extract_events
from market_analytics.sentiment.market import get_market_confirmation
from market_analytics.sentiment.models import MarketIntelligenceResult
from market_analytics.sentiment.sentiment import analyze_events
from market_analytics.sentiment.signal import calculate_signal
from market_analytics.sentiment.news import get_news
from market_analytics.clients.gemini import GeminiClient
from market_analytics.config.settings import settings

logger = logging.getLogger(__name__)


def run_sentiment(ticker, company_name):
    logger.info(f"Starting sentiment pipeline for {ticker}")

    articles = get_news(ticker)
    logger.info(f"Fetched {len(articles)} news articles for {ticker}")

    gemini_client = GeminiClient(settings.gemini_api_key)

    extraction = extract_events(
        ticker=ticker,
        company_name=company_name,
        articles=articles,
        gemini_client=gemini_client,
    )

    logger.info(f"Extracted {len(extraction.events)} market events for {ticker}")

    sentiment = analyze_events(
        ticker=ticker,
        company_name=company_name,
        events=extraction.events,
        gemini_client=gemini_client,
    )

    confirmation = get_market_confirmation(ticker)

    signal = calculate_signal(
        sentiment,
        extraction.events,
        confirmation,
    )

    price = float(yf.Ticker(ticker).history(period="1d").Close.iloc[-1])

    result = MarketIntelligenceResult(
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

    logger.info(
        f"Completed sentiment pipeline for {ticker}: signal={signal.signal}, classification={signal.classification}"
    )

    return result
