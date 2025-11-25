import feedparser
import json
import os

# Where we will save fetched articles (one JSON object per line)
OUT = "data/articles.json"
os.makedirs(os.path.dirname(OUT), exist_ok=True)

# ingest/fetch_rss.py (only change the feed_url line)
feed_url = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"

feed = feedparser.parse(feed_url)

# Append the first N entries to the file.
with open(OUT, "a", encoding="utf-8") as f:
    for entry in feed.entries[:10]:
        # entry is a dict-like object containing title, summary, link, etc.
        doc = {
            "title": entry.get("title", ""),
            "text": entry.get("summary", "") or entry.get("description", ""),
            "url": entry.get("link", "")
        }
        # write one JSON object per line (JSON Lines format)
        f.write(json.dumps(doc, ensure_ascii=False) + "\n")

print("Saved sample articles to", OUT)

