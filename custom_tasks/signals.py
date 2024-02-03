from django.contrib.auth.models import Permission
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Task, CeleryJobInfo
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .tasks import send_task_email
from celery.result import AsyncResult


@receiver(post_save, sender=get_user_model())
def assign_task_permissions(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        content_type = ContentType.objects.get_for_model(Task)
        permissions = Permission.objects.filter(content_type=content_type)
        instance.user_permissions.add(*permissions)


@receiver(post_save, sender=Task)
def schedule_send_task_email(sender, instance, created, **kwargs):
    # Schedule the send_task_email task when a Task is created or updated
    if created:
        # Task is being created
        result = send_task_email.apply_async(args=[instance.id], eta=instance.time_to_send)
        CeleryJobInfo.objects.create(
            task=instance,
            celery_job_id=result.id,
        )

    else:
        # Task is being updated, cancel the existing task and reschedule
        task = CeleryJobInfo.objects.get(task=instance)
        if task.celery_job_id:
            AsyncResult(task.celery_job_id).revoke() # Cancel existing task
        
        result = send_task_email.apply_async(args=[instance.id], eta=instance.time_to_send)  # Reschedule task
        job_info = CeleryJobInfo.objects.get(task=instance)
        job_info.celery_job_id=result.id
        job_info.save()