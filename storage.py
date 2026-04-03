import json
import os
import shutil
from datetime import datetime, timezone

from config import NEWS_FILE


def load_news():
    if not os.path.exists(NEWS_FILE):
        return {"last_updated": None, "articles": []}
    try:
        with open(NEWS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        backup = NEWS_FILE + ".bak"
        shutil.copy2(NEWS_FILE, backup)
        print(f"WARNING: Corrupted {NEWS_FILE}, backed up to {backup}")
        return {"last_updated": None, "articles": []}


def get_existing_titles(data):
    return {a["title"].strip().lower() for a in data.get("articles", [])}


def filter_new(articles, existing_titles):
    return [a for a in articles if a["title"].strip().lower() not in existing_titles]


def save_news(data, new_articles):
    data["articles"].extend(new_articles)
    data["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
