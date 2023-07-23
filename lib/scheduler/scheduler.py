from scheduler import Scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from abc import ABC, abstractmethod
import requests
import logging
import pytz
from dateutil import tz
from lib.common.constants import timezone

TIME_MASK = '%Y-%m-%dT%H:%M:%S.%fZ'

logger = logging.getLogger(__name__)

class TaskScheduler(ABC):

    def __init__(self):
        self.schedule = BackgroundScheduler(daemon=True)
        
    def __repr__(self) -> str:
        return str(self.schedule)

    @abstractmethod
    def send_message(self, message_text: str):
        pass

    @staticmethod
    def parse_time(datetime_str: str) -> datetime:
        datetime_dt = datetime.strptime(datetime_str, TIME_MASK)
        from_zone = tz.tzutc()
        to_zone = tz.gettz(timezone)
        datetime_dt = datetime_dt.replace(tzinfo=from_zone)
        datetime_local = datetime_dt.astimezone(to_zone)
        return datetime_local

    def add_task(self, task_id: str, task_name: str, task_time: str):
        
        task_datetime = self.parse_time(task_time)
        old_job = self.schedule.get_job(task_id)
        if old_job:
            self.schedule.remove_job(task_id)
        self.schedule.add_job(self.send_message, 'date', run_date=task_datetime, 
                                args=[task_name], id=task_id)
        logger.debug(f"added job {task_name} with {task_id} at {task_datetime=}")

    def delete_task(self, task_id: str):
        self.schedule.remove_job(task_id)

    def start_scheduling(self):
        self.schedule.start()


class TelegramScheduler(TaskScheduler):

    def __init__(self, token: str, chat_id: str):
        super().__init__()
        self._token = token
        self._chat_id = chat_id
        
    def send_message(self, message_text: str):
        apiURL = f'https://api.telegram.org/bot{self._token}/sendMessage'

        try:
            response = requests.post(apiURL, json={'chat_id': self._chat_id, 'text': message_text})
            if response.status_code != 200:
                logger.error(f"Couldnt send message with {message_text=}\n Error: {response.text}")
        except Exception as e:
            logger.error(f"Couldnt send message with {message_text=}\n Error: {e}")
