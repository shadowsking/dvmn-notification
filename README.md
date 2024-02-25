# dvmn-notification

Телеграм бот для уведомлений о проверенных задачах для сайта https://dvmn.org.

### Установка

```bash
git clone https://github.com/shadowsking/dvmn-notification.git
```

Создайте виртуальное окружение

```bash
python -m venv venv
source venv/scripts/activate
```

Установите зависимости
```bash
pip install -r requirements.txt
```

Создайте '.env' файл и установите следующие аргументы:
- DVMN_TOKEN
- TELEGRAM_TOKEN
- TELEGRAM_CHAT_ID


### Запуск
```bash
python main.py
```
#### Arguments:
- -t (--timeout): flot - Request timeout value in seconds
