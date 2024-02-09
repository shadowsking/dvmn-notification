import os
import time
from datetime import datetime
from pprint import pprint

import requests
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

    timestamp = datetime.now().timestamp()
    while True:
        try:
            notification = get_notification(os.environ["DVMN_TOKEN"], timestamp)
            timestamp = notification["last_attempt_timestamp"]
            pprint(notification)
        except requests.ReadTimeout as err:
            print(err)
        except requests.ConnectionError as err:
            pprint(err)
            time.sleep(30)
