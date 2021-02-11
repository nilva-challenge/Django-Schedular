from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Schedular.settings')
from django.conf import settings
app = Celery('Schedular')
# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    # Executes every day at  12:30 pm.
    'run-every-minutes': {
        'task': 'tasks.trigger_emails',
        'schedule':crontab(hour="*", minute="*", day_of_week="*"),
        'args': (),
    },
}