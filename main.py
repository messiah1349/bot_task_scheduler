from lib.scheduler import TelegramScheduler
import time

token = '214139458:AAH8UGU0PW3vUE1lRz-gjXnlB6TroUvpfUk'
chat_id = '46340594'

ts = TelegramScheduler(token, chat_id)
ts.add_task('1', 'posrat', '18.07.2023 19:57:05')
# print(ts.schedule)

print('startanuli!!')
while True:
    ts.start_scheduling()
    time.sleep(1)
