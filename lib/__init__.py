import logging
import datetime
from lib.utils.app_initializer import AppInitializer
from .common.constants import (TELEGRAM_TOKEN, CHAT_ID)
from lib.scheduler import TelegramScheduler

# clear handlers
root_logger = logging.root
root_logger.handlers.clear()

# init module logger
root_module_logger = logging.getLogger(__name__)
root_module_logger.setLevel(logging.DEBUG)

# format
formatter = logging.Formatter(
    '%(asctime)s - [worker %(process)d] - [%(name)s: %(levelname)s] - %(message)s'
)
logging.Formatter.formatTime = (
	lambda self, record, datefmt=None: datetime.datetime.fromtimestamp(record.created)
)

# add stdout handler
# stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler = logging.FileHandler('stdout_task_scheduler_log.txt', mode='a')
stdout_handler.addFilter(lambda entry: entry.levelno <= logging.INFO)
stdout_handler.setFormatter(formatter)
root_module_logger.addHandler(stdout_handler)

# add stderr handler
# stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler = logging.FileHandler('stderr_task_scheduler_log.txt', mode='a')
stderr_handler.addFilter(lambda entry: entry.levelno > logging.INFO)
stderr_handler.setFormatter(formatter)
root_module_logger.addHandler(stderr_handler)


root_module_logger.info("Logging was inited")


telegram_scheduler = TelegramScheduler(TELEGRAM_TOKEN, CHAT_ID)
telegram_scheduler.start_scheduling()
app = AppInitializer().get_app()
