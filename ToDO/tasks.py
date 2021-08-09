from __future__ import absolute_import, unicode_literals
from .celery import app
from main.models import Task
from datetime import datetime, timezone
from django.core.mail import send_mail


@app.task(name='send_emails')
def send_emails(): 
    date = datetime.now(timezone.utc).date()
    time = datetime.now(timezone.utc).time()
    scheduled_tasks = Task.objects.filter(time_to_send__date=date, 
                        time_to_send__time__hour=time.hour,
                        time_to_send__time__minute=time.minute)
                        
    for scheduled_task in scheduled_tasks:
        send_mail(
            'your task is done',
            f'task ({scheduled_task.title}) is done',
            'lyrdaq777@gmail.com',
            [scheduled_task.owner.email],
            fail_silently=False,
        )