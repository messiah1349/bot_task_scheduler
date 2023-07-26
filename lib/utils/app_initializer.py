from flask import Flask

class AppInitializer:

    def __init__(self):
        self._app = None

    def get_app(self):
        if self._app is None:
            self._app = Flask('task_scheduler')

        return self._app
