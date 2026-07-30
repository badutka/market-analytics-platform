import urllib.parse
import feedparser

from market_analytics.clients.http import session
from market_analytics.sentiment.constants import SOURCE_WEIGHTS

def get_news(ticker, limit=25):

    params = {
        "q": f"{ticker} stock financial news",
        "hl": "en-US",
        "gl": "US",
        "ceid": "US:en",
    }

    url = (
        "https://news.google.com/rss/search?"
        + urllib.parse.urlencode(params)
    )

    response = session.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 Chrome/120"
        },
        timeout=10,
    )

    response.raise_for_status()

    feed = feedparser.parse(response.content)

    articles = []

    for entry in feed.entries[:limit]:

        title = entry.title
        source = "Unknown"

        if " - " in title:
            title, source = title.rsplit(
                " - ",
                1,
            )

        articles.append(
            {
                "headline": title.strip(),
                "source": source.strip(),
                "weight": SOURCE_WEIGHTS.get(
                    source.strip(),
                    0.5,
                ),
            }
        )

    return articles


def format_news(articles):

    return "\n".join(
        f"""
Headline:
{a['headline']}

Source:
{a['source']}

Credibility:
{a['weight']}
"""
        for a in articles
    )