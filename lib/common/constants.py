import os

TELEGRAM_TOKEN = os.getenv("SCHEDULER_TELEGRAM_TOKEN", '')
CHAT_ID = os.getenv("CHAT_ID", "")
timezone = os.getenv("TZ" ,'Europe/Helsinki')
