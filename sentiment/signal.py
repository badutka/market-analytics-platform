from sentiment.models import SignalResult

SIGNAL_MODEL_NAME = "market_intelligence_signal"
SIGNAL_MODEL_VERSION = "0.1"
SIGNAL_STATUS = "experimental"


def calculate_signal(
    analysis,
    events,
    confirmation,
):

    positive_strength = 0
    negative_strength = 0

    for event in events:

        strength = (
            event.importance
            * event.novelty
            * event.factual_certainty
            * event.impact_certainty
        )

        if event.impact.value == "bullish":
            positive_strength += strength

        elif event.impact.value == "bearish":
            negative_strength += strength

    total_strength = positive_strength + negative_strength

    if total_strength > 0:

        uncertainty = min(
            positive_strength,
            negative_strength,
        ) / max(
            positive_strength,
            negative_strength,
        )

        event_balance = (positive_strength - negative_strength) / total_strength

    else:

        uncertainty = 0
        event_balance = 0

    confirmation_factor = 0.5 + confirmation.confirmation_score / 2

    signal = (
        event_balance
        * analysis.confidence
        * (1 - analysis.priced_in_probability)
        * confirmation_factor
    )

    return SignalResult(
        signal=round(signal, 3),
        positive_strength=round(
            positive_strength,
            3,
        ),
        negative_strength=round(
            negative_strength,
            3,
        ),
        uncertainty_score=round(
            uncertainty,
            3,
        ),
        classification=classify_signal(
            signal,
        ),
        interpretation=interpret_signal(
            signal,
            uncertainty,
            confirmation,
        ),
        model_name=SIGNAL_MODEL_NAME,
        model_version=SIGNAL_MODEL_VERSION,
        status=SIGNAL_STATUS,
    )


def classify_signal(signal):

    if signal > 0.25:
        return "Strong bullish"

    if signal > 0.10:
        return "Moderately bullish"

    if signal > -0.10:
        return "Neutral"

    if signal > -0.25:
        return "Moderately bearish"

    return "Strong bearish"


def interpret_signal(
    signal,
    uncertainty,
    confirmation,
):

    if uncertainty > 0.7:
        return "High uncertainty. " "Opposing catalysts detected."

    if signal > 0.25:
        return "Bullish setup with supportive catalysts."

    if signal < -0.25:
        return "Bearish setup with downside catalysts."

    if confirmation.confirmation_score < -0.2:
        return "News direction is not confirmed " "by market price action."

    return "No clear directional advantage."
