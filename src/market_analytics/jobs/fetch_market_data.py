import logging

import yfinance as yf
import pandas as pd

logger = logging.getLogger(__name__)


def clean_column_names(df):
    df.columns = [str(col).lower().strip().replace(" ", "_") for col in df.columns]
    return df


def fetch_market_prices(tickers, period):
    all_data = []

    logger.info(f"Starting market data download for {len(tickers)} tickers")

    for ticker in tickers:
        logger.info(f"Downloading {ticker}")

        try:
            df = yf.download(
                ticker,
                period=period,
                multi_level_index=False,
            )
        except Exception:
            logger.exception(f"Failed downloading {ticker}")
            continue

        if df.empty:
            logger.warning(f"No market data returned for {ticker}")
            continue

        df = df.reset_index()
        df = clean_column_names(df)
        df["ticker"] = ticker

        logger.info(f"Downloaded {len(df)} rows for {ticker}")

        all_data.append(df)

    if not all_data:
        logger.error("No market data collected")
        return None

    final_df = pd.concat(all_data, ignore_index=True)

    logger.info(f"Market data collection completed: {len(final_df)} total rows")

    return final_df
