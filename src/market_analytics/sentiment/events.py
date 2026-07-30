from google.genai import types

from market_analytics.sentiment.models import EventExtraction
from market_analytics.sentiment.news import format_news
from market_analytics.config.defaults import LLM_MODEL_NAME
from market_analytics.clients.gemini import GeminiClient


def extract_events(
    ticker: str,
    company_name: str,
    articles: list,
    gemini_client: GeminiClient,
):

    prompt = f"""
Analyze recent news about {company_name} ({ticker}).

Extract unique market moving events.

Rules:
- Do not remove repeated articles.
- Merge only identical events.
- Include bullish, bearish and neutral events.
- Separate facts from rumors.

Score:
importance
novelty
factual_certainty
impact_certainty

News:

{format_news(articles)}
"""
    response = gemini_client.generate(
        model=LLM_MODEL_NAME,
        prompt=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=EventExtraction,
            temperature=0,
        ),
    )

    return EventExtraction.model_validate_json(response.text)
