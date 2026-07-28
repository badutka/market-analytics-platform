import yfinance as yf

from sentiment.models import MarketConfirmation


def get_market_confirmation(ticker):

    history = yf.Ticker(ticker).history(
        period="30d"
    )

    latest = history.iloc[-1]
    previous = history.iloc[-2]

    daily_return = (
        latest.Close /
        previous.Close
        - 1
    )

    volume_change = (
        latest.Volume /
        history.Volume.tail(10).mean()
        - 1
    )

    volatility = (
        history.Close
        .pct_change()
        .tail(10)
        .std()
    )

    score = 0

    score += 0.2 if daily_return > 0 else -0.2

    if volume_change > 0.2:
        score += 0.4
    elif volume_change < -0.2:
        score -= 0.4

    if volatility > 0.03:
        score -= 0.1

    interpretation = (
        "Strong price confirmation"
        if score > 0.2
        else "Price action contradicts news"
        if score < -0.2
        else "Weak price confirmation"
    )

    return MarketConfirmation(
        daily_return=round(float(daily_return),4),
        volume_change=round(float(volume_change),4),
        volatility=round(float(volatility),4),
        confirmation_score=score,
        interpretation=interpretation,
    )