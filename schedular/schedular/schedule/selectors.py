from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from .models import Task
User = get_user_model()


def get_tasks(user: User) -> QuerySet[Task]:
    tasks = Task.objects.all() if user.is_staff or user.is_superuser else Task.objects.filter(owner=user)
    return tasks
