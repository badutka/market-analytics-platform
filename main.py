import pandas as pd

from market_analytics.jobs.fetch_market_data import fetch_market_prices
from market_analytics.jobs.run_sentiment import run_sentiment
from market_analytics.clients.bigquery import BigQueryClient
from market_analytics.config.logging import setup_logging
from market_analytics.config.settings import settings
from market_analytics.assets.markets import (
    TICKERS,
    COMPANIES,
)
from market_analytics.config.tables import (
    MARKET_TABLE,
    SENTIMENT_TABLE,
    EVENT_TABLE,
)

setup_logging(settings.log_level)


def main():
    bqc = BigQueryClient(project_id=settings.gcp_project_id)

    prices_df = fetch_market_prices(tickers=TICKERS, period="365d")

    bqc.write_dataframe(
        dataframe=prices_df,
        table=MARKET_TABLE,
        write_disposition="WRITE_TRUNCATE",
    )

    sentiment_records = []
    event_records = []

    for ticker, company in COMPANIES:

        result = run_sentiment(
            ticker,
            company,
        )

        sentiment_records.append(result.sentiment_record())

        event_records.extend(result.event_records())

    sentiment_df = pd.DataFrame(sentiment_records)
    events_df = pd.DataFrame(event_records)

    bqc.write_dataframe(
        dataframe=sentiment_df,
        table=SENTIMENT_TABLE,
        write_disposition="WRITE_TRUNCATE",
    )

    bqc.write_dataframe(
        dataframe=events_df,
        table=EVENT_TABLE,
        write_disposition="WRITE_TRUNCATE",
    )


if __name__ == "__main__":
    main()
