import logging
import time
from datetime import datetime, timezone

from news_fetcher import fetch_news
from translator import translate_title
from telegram_sender import send_news
from storage import load_news, get_existing_titles, filter_new, save_news

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting news scraper...")

    data = load_news()
    existing_titles = get_existing_titles(data)
    logger.info(f"Loaded {len(existing_titles)} existing articles")

    articles = fetch_news()
    logger.info(f"Fetched {len(articles)} total articles")

    new_articles = filter_new(articles, existing_titles)
    if not new_articles:
        logger.info("No new news found.")
        return

    logger.info(f"Found {len(new_articles)} new articles")

    sent_articles = []
    for article in new_articles:
        article["title_cn"] = translate_title(article["title"])
        article["found_at"] = datetime.now(timezone.utc).isoformat()

        if send_news(article):
            sent_articles.append(article)
            time.sleep(1)

    if sent_articles:
        save_news(data, sent_articles)
        logger.info(f"Done. Sent and saved {len(sent_articles)} new articles.")
    else:
        logger.info("No articles were successfully sent.")


if __name__ == "__main__":
    main()
