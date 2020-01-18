from celery import shared_task
from app.utils import update_task


@shared_task
def hello():
    print('Hello there!')
    return 'Hello there!'


@shared_task
def update_task_ctask(id):
    return update_task(id)
