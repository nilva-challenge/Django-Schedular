from celery import shared_task, current_task
from time import sleep
from celery.contrib import rdb
from django.core.mail import send_mail

MESSAGE = 'This is from you task schedule Nilva. You scheduled this time for  your task. Thanks for using Nilva'


@shared_task
def send_task_mail(email):
    msg = send_mail(
        subject='Schedule Nilva',
        message=MESSAGE,
        from_email=None,
        recipient_list=[email],
        fail_silently=False)
    return msg
