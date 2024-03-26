import logging

import telegram

import settings


class TelegramLogsHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.bot = telegram.Bot(token=settings.TELEGRAM_LOGGER_TOKEN)

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(
            chat_id=settings.TELEGRAM_CHAT_ID,
            text=log_entry
        )


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)

    handler = TelegramLogsHandler()
    logger.addHandler(handler)

    return logger
