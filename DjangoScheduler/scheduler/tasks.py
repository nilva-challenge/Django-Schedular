from celery import shared_task

from django.core.mail import send_mail
from time import sleep


@shared_task()
def send_email_task(title, description, email):
    send_mail(title,
              description,
              'bmhztest@fastmail.com',
              [email])

    return 'DONE'
