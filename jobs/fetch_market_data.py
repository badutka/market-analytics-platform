import yfinance as yf
import pandas as pd


def clean_column_names(df):

    df.columns = [str(col).lower().strip().replace(" ", "_") for col in df.columns]

    return df


def fetch_market_prices(tickers):

    all_data = []

    for ticker in tickers:

        print(f"Downloading {ticker}")

        df = yf.download(
            ticker,
            period="365d",
            multi_level_index=False,
        )

        if df.empty:
            continue

        df = df.reset_index()

        df = clean_column_names(df)

        df["ticker"] = ticker

        all_data.append(df)

    if not all_data:
        return

    final_df = pd.concat(
        all_data,
        ignore_index=True,
    )

    return final_df
