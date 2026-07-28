from sentiment.pipeline import run_pipeline


def main():
    result = run_pipeline(
        ticker="AAPL",
        company_name="Apple Inc.",
    )

    print("\nSentiment record:")
    print(result.sentiment_record())

    print("\nEvent records:")
    for event in result.event_records():
        print(event)


if __name__ == "__main__":
    main()
