import feedparser

feeds = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://rss.theguardian.com/theguardian/world/rss",
    "https://feeds.reuters.com/reuters/topNews"
]

for url in feeds:
    feed = feedparser.parse(url)
    for entry in feed.entries[:3]:
        print(entry.title, entry.published)
