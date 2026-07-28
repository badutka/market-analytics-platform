from google.genai import types

from sentiment.config import client, MODEL_NAME
from sentiment.models import EventExtraction
from sentiment.news import format_news


def extract_events(
    ticker,
    company_name,
    articles,
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

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=EventExtraction,
            temperature=0,
        ),
    )

    return EventExtraction.model_validate_json(
        response.text
    )