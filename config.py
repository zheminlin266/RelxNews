import os

KEYWORDS = ["Relx", "RLX", "Vaping Regulation", "China vaping"]

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = "-5276723831"

NEWS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news_lists.json")

GNEWS_PERIOD = "7d"
