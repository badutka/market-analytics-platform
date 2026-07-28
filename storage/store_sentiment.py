import pandas as pd

from storage.bigquery import load_dataframe

SENTIMENT_TABLE = "ms-fin-analytics-dev.analytics.market_sentiment"

EVENT_TABLE = "ms-fin-analytics-dev.analytics.market_events"


def save_sentiment(result):

    sentiment_df = pd.DataFrame([result.sentiment_record()])

    events_df = pd.DataFrame(result.event_records())

    load_dataframe(
        sentiment_df,
        SENTIMENT_TABLE,
    )

    load_dataframe(
        events_df,
        EVENT_TABLE,
    )
