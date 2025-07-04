import feedparser


def fetch_latest_news():
    feeds = [
        "https://dev.to/feed/",
        "https://www.theverge.com/rss/index.xml",
        "https://www.wired.com/feed/rss",
        "https://investnews.com.br/feed/",
    ]
    noticias = []

    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            noticias.append(
                {
                    "title": entry.title,
                    "link": entry.link,
                    "content": (
                        entry.summary if hasattr(entry, "summary") else entry.title
                    ),
                }
            )

    return noticias
