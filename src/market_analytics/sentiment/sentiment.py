from google.genai import types

from market_analytics.sentiment.models import EventAnalysis
from market_analytics.config.defaults import LLM_MODEL_NAME
from market_analytics.clients.gemini import GeminiClient

def analyze_events(
    ticker: str,
    company_name: str,
    events: list,
    gemini_client: GeminiClient
):

    text = "\n".join(
        f"""
Event:
{e.event}

Impact:
{e.impact.value}

Importance:
{e.importance}

Novelty:
{e.novelty}

Certainty:
{e.factual_certainty}
"""
        for e in events
    )

    prompt = f"""
Analyze investment outlook for {company_name}.

Return:

sentiment_score
confidence
priced_in_probability

Events:

{text}
"""

    response = gemini_client.generate(
        model=LLM_MODEL_NAME,
        prompt=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=EventAnalysis,
            temperature=0,
        ),
    )

    return EventAnalysis.model_validate_json(
        response.text
    )