COMPANIES = [
    ("AAPL", "Apple Inc."),
    ("MSFT", "Microsoft Corporation"),
    ("NVDA", "NVIDIA Corporation"),
    ("JPM", "JPMorgan Chase & Co."),
    ("AMZN", "Amazon.com, Inc."),
    ("BTC-USD", "Bitcoin"),
]

TICKERS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "JPM",
    "AMZN",
    "BTC-USD",
]

FINNHUB_SYMBOL_MAP = {
    "BTC-USD": "BINANCE:BTCUSDT",
    "ETH-USD": "BINANCE:ETHUSDT",
}

DASHBOARD_ASSETS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "GOOGL",
    "TSLA",
    "BTC-USD",
    "ETH-USD",
]


STOCK_TICKERS = [
    ticker
    for ticker in DASHBOARD_ASSETS
    if ticker
    not in {
        "BTC-USD",
        "ETH-USD",
    }
]


CRYPTO_TICKERS = [ticker for ticker in DASHBOARD_ASSETS if ticker not in STOCK_TICKERS]
