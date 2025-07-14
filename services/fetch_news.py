import feedparser
import time


def fetch_latest_news():
    feeds = [
        "https://dev.to/feed/",
        "https://www.theverge.com/rss/index.xml",
        "https://www.wired.com/feed/rss",
        "https://investnews.com.br/feed/",
    ]
    noticias = []
    hoje = time.localtime()
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            if hasattr(entry, "published_parsed"):
                publicado = entry.published_parsed
                if (
                    publicado.tm_year == hoje.tm_year
                    and publicado.tm_mon == hoje.tm_mon
                    and publicado.tm_mday == hoje.tm_mday
                ):

                    noticias.append(
                        {
                            "title": entry.title,
                            "link": entry.link,
                            "content": (
                                entry.summary
                                if hasattr(entry, "summary")
                                else entry.title
                            ),
                        }
                    )

    return noticias
