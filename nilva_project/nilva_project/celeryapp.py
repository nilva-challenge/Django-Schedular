from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nilva_project.settings')

celery_app = Celery('nilva_project')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks()
