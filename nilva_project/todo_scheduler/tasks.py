from celery import shared_task
from django.core.mail import EmailMessage,send_mail



@shared_task
def send_reminder_email(email):
    subject = 'Reminder !!'
    message = "you set a reminder for current time !"
    my_email = "write your email here"
    send_mail(
        subject = subject,
        message = message,
        from_email =  my_email,
        recipient_list = [email,]
    )