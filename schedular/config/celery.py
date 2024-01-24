import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django.local')

celery = Celery('config')
celery.config_from_object('django.conf:django', namespace='CELERY')
celery.autodiscover_tasks(['schedular.schedule.tasks'])
# celery.autodiscover_tasks()