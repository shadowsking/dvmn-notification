import argparse
import os
import time
from datetime import datetime

import requests
import telegram
from dotenv import load_dotenv


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
    load_dotenv()

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

    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
    timestamp = datetime.now().timestamp()
    while True:
        try:
            notification = get_notification(
                os.environ["DVMN_TOKEN"], timestamp, timeout=args.timeout
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
                    chat_id=os.environ["TELEGRAM_CHAT_ID"],
                    text=text,
                    parse_mode="Markdown",
                )
        except requests.ReadTimeout as err:
            continue
        except requests.ConnectionError as err:
            print(err)
            time.sleep(30)
