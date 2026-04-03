import logging
import time
import requests

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

logger = logging.getLogger(__name__)

SEND_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_news(article):
    title = article["title"]
    title_cn = article["title_cn"]
    publisher = article.get("publisher", "Unknown")
    keyword = article.get("keyword", "")
    url = article.get("url", "")

    text = (
        "<b>New Vaping News / 电子烟新闻</b>\n\n"
        f"<b>Title:</b> {_escape_html(title)}\n"
        f"<b>标题翻译:</b> {_escape_html(title_cn)}\n"
        f"<b>Source:</b> {_escape_html(publisher)}\n"
        f"<b>Keyword:</b> {_escape_html(keyword)}\n\n"
        f'<a href="{url}">Read more / 阅读更多</a>'
    )

    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }

    for attempt in range(2):
        try:
            resp = requests.post(SEND_URL, json=payload, timeout=15)
            data = resp.json()

            if data.get("ok"):
                logger.info(f"Sent: {title}")
                return True

            if resp.status_code == 429:
                retry_after = data.get("parameters", {}).get("retry_after", 5)
                logger.warning(f"Rate limited, retrying after {retry_after}s")
                time.sleep(retry_after)
                continue

            logger.error(f"Telegram API error: {data}")
            return False

        except Exception as e:
            logger.error(f"Failed to send message (attempt {attempt + 1}): {e}")
            if attempt == 0:
                time.sleep(3)

    return False


def _escape_html(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
