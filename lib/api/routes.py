from flask import request
from lib import app, telegram_scheduler


@app.route('/api/v1/add_task/', methods = ['POST'])
def add_task():
    input_data = request.get_json()
    telegram_scheduler.add_task(input_data['id'], input_data['name'], input_data['due'])
    return f"{input_data=}"

@app.route('/api/v1/delete_task/', methods = ['DELETE'])
def delete_task():
    input_data = request.get_json()
    telegram_scheduler.delete_task(input_data['id'])
    return f"{input_data=}"

@app.route('/health/')
def health():
    return 'OK!'

