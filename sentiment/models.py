from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from sentiment.config import MODEL_NAME


class Impact(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


class MarketEvent(BaseModel):
    event: str
    impact: Impact
    importance: float = Field(ge=0, le=1)
    novelty: float = Field(ge=0, le=1)
    factual_certainty: float = Field(ge=0, le=1)
    impact_certainty: float = Field(ge=0, le=1)
    explanation: str


class EventExtraction(BaseModel):
    events: list[MarketEvent]


class EventAnalysis(BaseModel):
    sentiment_score: float
    confidence: float
    priced_in_probability: float
    bullish_factors: list[str]
    bearish_factors: list[str]
    reasoning: str


class MarketConfirmation(BaseModel):
    daily_return: float
    volume_change: float
    volatility: float
    confirmation_score: float
    interpretation: str


class SignalResult(BaseModel):
    signal: float
    positive_strength: float
    negative_strength: float
    uncertainty_score: float
    classification: str
    interpretation: str
    model_name: str
    model_version: str
    status: str


class MarketIntelligenceResult(BaseModel):
    analysis_id: str
    ticker: str
    company_name: str
    timestamp: datetime
    price: float

    sentiment: EventAnalysis
    signal: SignalResult
    market_confirmation: MarketConfirmation

    events: list[MarketEvent]
    articles: list[dict]

    def sentiment_record(self):
        return {
            "analysis_id": self.analysis_id,
            "ticker": self.ticker,
            "company_name": self.company_name,
            "timestamp": self.timestamp,
            "price": self.price,

            "sentiment_score": self.sentiment.sentiment_score,
            "confidence": self.sentiment.confidence,
            "priced_in_probability": self.sentiment.priced_in_probability,

            "positive_strength": self.signal.positive_strength,
            "negative_strength": self.signal.negative_strength,
            "uncertainty_score": self.signal.uncertainty_score,

            "signal": self.signal.signal,
            "classification": self.signal.classification,
            "interpretation": self.signal.interpretation,

            "signal_model_name": self.signal.model_name,
            "signal_model_version": self.signal.model_version,
            "signal_status": self.signal.status,

            "daily_return": self.market_confirmation.daily_return,
            "volume_change": self.market_confirmation.volume_change,
            "volatility": self.market_confirmation.volatility,
            "confirmation_score": self.market_confirmation.confirmation_score,
            "confirmation_interpretation": self.market_confirmation.interpretation,

            "bullish_factors": self.sentiment.bullish_factors,
            "bearish_factors": self.sentiment.bearish_factors,
            "reasoning": self.sentiment.reasoning,

            "pipeline_version": "v1",
            "signal_experimental": True,
            "model_name": MODEL_NAME,
        }

    def event_records(self):
        return [
            {
                "analysis_id": self.analysis_id,
                "ticker": self.ticker,
                "company_name": self.company_name,
                "timestamp": self.timestamp,
                **event.model_dump(),
                "impact": event.impact.value,
            }
            for event in self.events
        ]