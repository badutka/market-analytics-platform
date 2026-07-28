from jobs.fetch_market_data import fetch_market_prices
from jobs.run_sentiment import run_sentiment
from storage.store_market import save_market_prices
from storage.store_sentiment import save_sentiment

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


COMPANIES = [
    ("AAPL", "Apple Inc."),
    ("BTC-USD", "Bitcoin"),
    ("PKN.WA", "PKN Orlen"),
]

TICKERS = [
    "AAPL",
    "BTC-USD",
    "PKN.WA",
]


def main():
    # Fetch OHLCV data
    prices_df = fetch_market_prices(tickers=TICKERS)

    # Save OHLCV data
    save_market_prices(df=prices_df)

    # Run sentiment and store results
    for ticker, company in COMPANIES:

        result = run_sentiment(
            ticker,
            company,
        )

        save_sentiment(result)


if __name__ == "__main__":
    main()
