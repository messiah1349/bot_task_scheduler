from lib.scheduler import TelegramScheduler
from ..common.constants import (TELEGRAM_TOKEN, CHAT_ID)
from flask import Flask

class AppInitializer:

    _app = Flask('task_scheduler')

    def __init__(self):
        self.telegram_scheduler = TelegramScheduler(TELEGRAM_TOKEN, CHAT_ID)
        self._app = None

    def health(self):
        return "OK"

    def get_app(self):
        if self._app is None:
            self._app = Flask('task_scheduler')

        return self._app
