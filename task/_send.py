from datetime import datetime
from .models import Task
from django.core.mail import send_mail


def send_emails():

    current_time = datetime.now().strftime("%H:%M")
    tasks = Task.objects.all()

    for i in tasks:

        if i.time_to_send == current_time:

            send_mail(
                "Django Schedular",
                "Your task's time has come ",
                "Your Email",
                [i.owner.email],
            )

    return None
