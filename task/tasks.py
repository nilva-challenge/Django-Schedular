from datetime import timedelta
from uuid import UUID

from django.utils.timezone import now

from config import celery_app
from task.models import Task


@celery_app.task()
def send_task_email(task_id: UUID):
    task = Task.objects.get(id=task_id)
    task.send_email()
    return {"status": True}


@celery_app.task()
def send_tasks_email():
    now_time = now()
    min_time = now_time - timedelta(seconds=60)
    max_time = now_time + timedelta(seconds=60)
    tasks = Task.objects.filter(
        send_time_done__isnull=True,
        send_time_schedule__gte=min_time,
        send_time_schedule__lte=max_time,
    )
    for task in tasks:
        # send_task_email.delay(task)
        send_task_email.apply_async([task.id])

    return {"count": len(tasks)}
