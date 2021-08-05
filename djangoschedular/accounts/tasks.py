from django.core.mail import send_mail
from celery import shared_task
from datetime import datetime
from .models import Tasks

@shared_task()
def show():
    current_time = datetime.now().strftime("%H:%M")
    tasks = Tasks.objects.all()

    for i in tasks:

        if i.time_to_send == current_time:
            send_mail("Django Schedular","Your task's time has come ","Your Email",[i.owner.email],)
    return None