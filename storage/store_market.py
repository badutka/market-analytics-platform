from storage.bigquery import load_dataframe

MARKET_TABLE = "ms-fin-analytics-dev.raw_data.historical_market_prices"


def save_market_prices(df):

    load_dataframe(
        df,
        MARKET_TABLE,
        write_disposition="WRITE_APPEND",
    )