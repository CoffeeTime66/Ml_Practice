import requests
from redis import Redis
from celery import Celery
from kombu import Queue


model_to_money = {0: 10, 1: 15, 2: 20}
predict_url = "http://127.0.0.1:8936/predict"
redis_connection = Redis()

celery = Celery('tasks', broker='redis://localhost:6379/0')

# Register the high-priority queue
celery.conf.task_queues = [
    Queue('high', routing_key='high'),
]


@celery.task(name='utils.tasks.process_response', queue='high')
def process_response(data):
    response = requests.post(predict_url, json=data)
    if response.status_code == 200:
        result = response.json()["prediction"][0]
    else:
        result = None
    register_url = "http://127.0.0.1:8935/add_row"  
    data_to_send = {
        "user_id": data["user_id"],
        "model": data["model"],
        "age_group": data["age_group"],
        "RIAGENDR": data["RIAGENDR"],
        "PAQ605": data["PAQ605"],
        "BMXBMI": data["BMXBMI"],
        "LBXGLU": data["LBXGLU"],
        "DIQ010": data["DIQ010"],
        "LBXGLT": data["LBXGLT"],
        "LBXIN": data["LBXIN"],
        "result": result,
    }
    requests.post(register_url, json=data_to_send)
    return data_to_send 
    