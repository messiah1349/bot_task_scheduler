from scheduler import Scheduler
from datetime import datetime
from abc import ABC, abstractmethod
import requests

TIME_MASK = '%d.%m.%Y %H:%M:%S'


class TaskScheduler(ABC):

    def __init__(self):
        self.schedule = Scheduler()
        
    def __repr__(self) -> str:
        return str(self.schedule)

    @abstractmethod
    def send_message(self, message_text: str):
        pass

    @staticmethod
    def parse_time(datetime_str: str) -> datetime:
        return datetime.strptime(datetime_str, TIME_MASK)

    def add_task(self, task_id: str, task_name: str, task_time: str):

        task_datetime = self.parse_time(task_time)
        self.schedule.once(
            task_datetime, 
            self.send_message,
            kwargs={'message_text': task_name}, 
            tags={task_id}
        )

    def remove_task(self, task_id: str):
        pass

    def start_scheduling(self):
        self.schedule.exec_jobs()


class TelegramScheduler(TaskScheduler):

    def __init__(self, token: str, chat_id: str):
        super().__init__()
        self._token = token
        self._chat_id = chat_id
        
    def send_message(self, message_text: str):
        apiURL = f'https://api.telegram.org/bot{self._token}/sendMessage'
        # self.bot.send_message(chat_id=46340594, text = message_text)

        try:
            response = requests.post(apiURL, json={'chat_id': self._chat_id, 'text': message_text})
            # print(response.text)
        except Exception as e:
            print(e)

