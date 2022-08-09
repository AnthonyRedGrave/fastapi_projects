import time
import os
from celery import Celery
from celery.utils.log import get_task_logger

celery = Celery('tasks', broker="redis://redis:6379/0")
# celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
# celery.conf.broker_url = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

@celery.task(name="create_task")
def create_task(arg):
    print("WORKER", arg)
    print(1)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    print(" Я ТУТУ ")
    sender.add_periodic_task(1.0, create_task.s('hello'), name='Вщштп')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(10.0, create_task.s('world'), expires=10)
