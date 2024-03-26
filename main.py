import argparse
import time
from datetime import datetime

import requests
import telegram

import settings
from logger import get_logger

logger = get_logger("telegram_logger")


def get_notification(token, timestamp, timeout=None):
    response = requests.get(
        "https://dvmn.org/api/long_polling/",
        params={"timestamp": timestamp},
        headers={"Authorization": f"Token {token}"},
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Telegram bot for notifications about tasks"
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        help="Timeout value in seconds",
        default=5,
    )
    args = parser.parse_args()

    bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)
    logger.info("Бот запущен")

    timestamp = datetime.now().timestamp()
    while True:
        try:
            notification = get_notification(
                settings.DVMN_TOKEN, timestamp, timeout=args.timeout
            )
            if notification["status"] == "timeout":
                timestamp = notification["timestamp_to_request"]
                continue

            timestamp = notification["last_attempt_timestamp"]
            for attempt in notification["new_attempts"]:
                text = f"У вас проверили работу «[{attempt.get('lesson_title')}]({attempt.get('lesson_url')})»."
                if attempt["is_negative"]:
                    text += "\nВ работе нашлись ошибки!"
                else:
                    text += "\nМожно приступать к следующему уроку!"

                bot.send_message(
                    chat_id=settings.TELEGRAM_CHAT_ID,
                    text=text,
                    parse_mode="Markdown",
                )
        except requests.ReadTimeout as err:
            continue
        except requests.ConnectionError as err:
            logger.exception(err)
            time.sleep(30)
        except Exception as ex:
            raise logger.exception(f"Бот упал с ошибкой: {ex}")
