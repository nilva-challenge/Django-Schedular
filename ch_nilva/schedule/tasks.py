from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from ch_nilva.settings import EMAIL_HOST_USER


@shared_task()
def sleepy(duration):
    sleep(duration)
    return None


MESSAGE = 'This is from you task schedule Nilva. Your Times of Your task is come ...'


@shared_task(name='send_email')
def send_mail():
    send_mail(
        'Schedule Nilva',
        MESSAGE,
        EMAIL_HOST_USER,
        ['sadraproton@gmail.com'],
        fail_silently=False)
    return None
