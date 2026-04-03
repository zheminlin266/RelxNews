import logging
import urllib.parse
import xml.etree.ElementTree as ET
import requests

from config import KEYWORDS, GNEWS_PERIOD

logger = logging.getLogger(__name__)

GOOGLE_NEWS_RSS = "https://news.google.com/rss/search"


def _build_url(keyword):
    query = keyword
    if GNEWS_PERIOD:
        query += f" when:{GNEWS_PERIOD}"
    params = {
        "q": query,
        "hl": "en",
        "gl": "US",
        "ceid": "US:en",
    }
    return f"{GOOGLE_NEWS_RSS}?{urllib.parse.urlencode(params)}"


def _parse_rss(xml_text):
    articles = []
    root = ET.fromstring(xml_text)
    for item in root.iter("item"):
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        pub_date = item.findtext("pubDate", "").strip()

        source_el = item.find("source")
        publisher = source_el.text.strip() if source_el is not None and source_el.text else "Unknown"

        if title:
            articles.append({
                "title": title,
                "url": link,
                "publisher": publisher,
                "published_date": pub_date,
            })
    return articles


def fetch_news():
    all_articles = []
    seen_titles = set()

    for keyword in KEYWORDS:
        try:
            url = _build_url(keyword)
            resp = requests.get(url, timeout=15, headers={
                "User-Agent": "Mozilla/5.0 (compatible; NewsBot/1.0)"
            })
            resp.raise_for_status()
            entries = _parse_rss(resp.text)
            logger.info(f"Keyword '{keyword}': found {len(entries)} articles")

            for entry in entries:
                title = entry["title"]
                if title.lower() in seen_titles:
                    continue
                seen_titles.add(title.lower())
                entry["keyword"] = keyword
                all_articles.append(entry)

        except Exception as e:
            logger.warning(f"Failed to fetch news for keyword '{keyword}': {e}")

    return all_articles
