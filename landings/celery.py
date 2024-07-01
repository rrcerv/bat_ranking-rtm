# django_db_task/celery.py

import os
from celery import Celery

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 
    'django_bg_task.settings'
)

app = Celery('django_bg_task')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()