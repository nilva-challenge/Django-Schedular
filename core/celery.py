import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

celery_app = Celery('core', backend='redis://localhost', broker='redis://localhost:6378/0')

celery_app.conf.result_backend = f"rpc://redis:6378/3"
celery_app.conf.timezone = 'Asia/Tehran'
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'json'
celery_app.conf.accept_content = ['json']
celery_app.conf.task_always_eager = False
celery_app.conf.worker_prefetch_multiplier = 1
celery_app.autodiscover_tasks(['users.tasks'])
