from celery import shared_task
from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Task, CeleryJobInfo, TaskValidator
from django.conf import settings


import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)



@shared_task
def send_task_email(task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        logger.error(f'task object with id: {task_id} dose not exist')
        raise Task.DoesNotExist
    
    try:
        celery_job = CeleryJobInfo.objects.get(task=task)
    except CeleryJobInfo.DoesNotExist:
        logger.error(f'task object with task_id: {task_id} dose not exist')
        raise CeleryJobInfo.DoesNotExist
    
    validate = TaskValidator(task)
    if not validate.is_valid:
        logger.error(f'task object with task_id: {task_id} is not a valid task')
        raise Exception
    
    from_email = settings.EMAIL
    subject = f"Task Reminder: {task.title}"
    message = f"Dear {task.owner.username},\n\nThis is a reminder for your task: {task.title}\n\nDescription: {task.description}"
    try:
        send_mail(
            subject,
            message,
            from_email,
        [task.owner.email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f'some unexpected error happend. detail: \n {e}')
        celery_job.state = 'Failed'
        celery_job.save()
        raise Exception
    
    celery_job.state = 'Done'
    celery_job.save()

    
    
    

