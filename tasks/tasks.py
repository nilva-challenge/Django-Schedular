from celery import shared_task
from django.core.mail import send_mail
from .models import Task

@shared_task
def send_task_email(task_id):
    try:
        task = Task.objects.get(id=task_id)
        subject = f'Task Reminder: {task.title}'
        message = f'Hi {task.owner.username},\n\nThis is a reminder for your task: {task.title}.\n\nDescription: {task.description}'
        email_from = 'some_email@example.com'  # Replace with a dummy or actual sender email address
        recipient_list = [task.owner.email,]
        send_mail(subject, message, email_from, recipient_list)
    except Task.DoesNotExist:
        print(f'Task with id {task_id} does not exist.')
