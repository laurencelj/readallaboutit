import os
import sys
from dotenv import load_dotenv

# 1. Load the environment variables immediately
load_dotenv()

# 2. Dynamically find the project root 'src' directory
current_dir = os.path.dirname(os.path.abspath(__file__))  # src/readallaboutit
src_dir = os.path.dirname(current_dir)                    # src
sys.path.insert(0, src_dir)

# 3. NOW safely import your local modules and external dependencies
import feedparser
import hashlib
import yaml
from datetime import datetime, timezone
from readallaboutit.store import store_articles

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), '..', '..', 'config', 'feeds.yaml'
)

def load_feeds():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)['feeds']

def parse_entry(entry, feed, category):
    return {
        "id": hashlib.md5(entry.link.encode()).hexdigest(),
        "title": entry.title,
        "summary": entry.get("summary", ""),
        "published": entry.get("published", ""),
        "source": feed.feed.title,
        "url": entry.link,
        "category": category,
        "fetched_at": datetime.now(timezone.utc).isoformat()
    }

def fetch_articles():
    articles = []
    for feed_config in load_feeds():
        feed = feedparser.parse(feed_config['url'])
        for entry in feed.entries:
            articles.append(parse_entry(entry, feed, feed_config['category']))
    return articles

def deduplicate(articles):
    seen = set()
    unique = []
    for a in articles:
        if a['id'] not in seen:
            seen.add(a['id'])
            unique.append(a)
    return unique

def run():
    articles = fetch_articles()
    print(f"Fetched {len(articles)} articles")
    unique = deduplicate(articles)
    print(f"Unique articles: {len(unique)}")
    stored = store_articles(unique)
    print(f"Stored {stored} articles")

if __name__ == "__main__":
    run()
