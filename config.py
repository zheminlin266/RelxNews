import os

KEYWORDS = ["Relx", "RLX", "Vaping Regulation"]

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = "-5106544699"

NEWS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news_lists.json")

GNEWS_PERIOD = "7d"
