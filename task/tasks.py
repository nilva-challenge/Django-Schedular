from celery import shared_task
from ._send import send_emails


@shared_task
def send():
    send_emails()
