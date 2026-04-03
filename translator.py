import logging
import time
from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)

_translator = GoogleTranslator(source="auto", target="zh-CN")


def translate_title(title):
    try:
        result = _translator.translate(title)
        time.sleep(0.5)
        return result if result else title
    except Exception as e:
        logger.warning(f"Translation failed for '{title}': {e}")
        return f"[Translation Failed] {title}"
