from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from .tasks import send_email_task
from .models import Task
import datetime

User = get_user_model()


def get_tasks(user: User) -> QuerySet[Task]:
    tasks = Task.objects.all() if user.is_superuser else Task.objects.filter(owner=user)
    return tasks


def get_tasks_to_run() -> None:
    now = datetime.datetime.now()
    one_minute_later = now + datetime.timedelta(minutes=1)
    tasks = Task.objects.filter(time_to_send__range=(now, one_minute_later), sent=False)

    for task in tasks:
        send_email_task.apply_async([task.id])
