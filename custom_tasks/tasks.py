from celery import shared_task
from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Task
from django.conf import settings



@shared_task
def send_task_email(task_id):
    task = Task.objects.get(id=task_id)
    
    from_email = settings.EMAIL
    subject = f"Task Reminder: {task.title}"
    message = f"Dear {task.owner.username},\n\nThis is a reminder for your task: {task.title}\n\nDescription: {task.description}"
    
    send_mail(
        subject,
        message,
        from_email,
       [task.owner.email],
        fail_silently=False,
    )

