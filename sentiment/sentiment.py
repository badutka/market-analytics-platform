from google.genai import types

from sentiment.config import client, MODEL_NAME
from sentiment.models import EventAnalysis


def analyze_events(
    ticker,
    company_name,
    events,
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

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=EventAnalysis,
            temperature=0,
        ),
    )

    return EventAnalysis.model_validate_json(
        response.text
    )