from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ToDO.settings")

app = Celery('ToDO')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'trigger_emails': {
        'task': 'send_emails',
        'schedule': 60.0,
    },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))