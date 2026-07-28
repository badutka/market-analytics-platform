from sentiment.pipeline import run_pipeline


def run_sentiment(
    ticker,
    company_name,
):

    return run_pipeline(
        ticker=ticker,
        company_name=company_name,
    )