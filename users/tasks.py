from celery import shared_task
from users.models import Task
from users.emails import send_email_for_tasks


@shared_task
def send_task_email(task_id):

    task = Task.objects.get(id=task_id)
    if task.precondition_tasks():
        send_email_for_tasks(subject=task.title, message=task.description, recipient_list=[task.owner.email])
    task.save()

