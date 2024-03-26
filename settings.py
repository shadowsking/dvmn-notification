import os

import dotenv

dotenv.load_dotenv()

DVMN_TOKEN = os.environ["DVMN_TOKEN"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_LOGGER_TOKEN = os.environ["TELEGRAM_LOGGER_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
