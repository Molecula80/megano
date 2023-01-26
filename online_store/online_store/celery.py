import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_store.settings')
celery_app = Celery('online_store')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
