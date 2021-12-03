from celery import Celery

broker_url = 'redis://localhost:6379/0'
celery_result_backend = 'redis://localhost:6379/0'
app = Celery('tasks_practice', broker=broker_url,
             backend=celery_result_backend)


@app.task
def add(x, y):
    return x + y
