import os
import time
from datetime import datetime

import requests
import telegram
from dotenv import load_dotenv


def get_notification(token, timestamp):
    response = requests.get(
        "https://dvmn.org/api/long_polling/",
        params={"timestamp": timestamp},
        headers={"Authorization": f"Token {token}"},
    )
    response.raise_for_status()

    notification = response.json()
    if notification.get("status") == "timeout":
        raise requests.ReadTimeout("The server did not return anything")

    return notification


if __name__ == "__main__":
    load_dotenv()

    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
    timestamp = datetime.now().timestamp()
    while True:
        try:
            notification = get_notification(os.environ["DVMN_TOKEN"], timestamp)
            timestamp = notification["last_attempt_timestamp"]
            for attempt in notification["new_attempts"]:
                text = f"У вас проверили работу «[{attempt.get('lesson_title')}]({attempt.get('lesson_url')})»."
                if attempt["is_negative"]:
                    text += "\nВ работе нашлись ошибки!"
                else:
                    text += "\nМожно приступать к следующему уроку!"

                bot.send_message(
                    chat_id=os.environ["CHAT_ID"], text=text, parse_mode="Markdown"
                )
        except requests.ReadTimeout as err:
            print(err)
        except requests.ConnectionError as err:
            print(err)
            time.sleep(30)
