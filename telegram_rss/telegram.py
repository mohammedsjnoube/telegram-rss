import logging
from telegram import Bot, ParseMode
from time import sleep
from typing import List

from telegram_rss.config import Config
from telegram_rss.feed import FeedUpdater

logger = logging.getLogger(__name__)


def send_message(bot: Bot, text: str, chat_ids: List[int]):
    for chat_id in chat_ids:
        bot.send_message(chat_id, str(text), parse_mode=ParseMode.HTML)
        sleep(0.05)


def send_update(bot: Bot, config: Config):
    chat_ids = config.channels + config.users
    for feed_config in config.feeds:
        updater = FeedUpdater(feed_config)
        entries = updater.get_new_entries()
        entries.reverse()
        for entry in entries:
            send_message(bot, str(entry), chat_ids)
        sleep(3.0)
