from celery import shared_task, Celery
from django.core.mail import send_mail
from django.conf import settings
from .models import Task
import datetime

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@shared_task
def send_email_to_owners():
    tasks = Task.objects.all()
    for task in tasks:
        if task.time_to_send == datetime.datetime.now().strftime("%Y-%m-%d %H:%M"):
            send_mail(subject="task manager", message="task should be done now!",
                      from_email=settings.DEFAULT_FROM_EMAIL,
                      recipient_list=[task.owner.email])




