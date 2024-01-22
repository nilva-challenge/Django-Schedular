from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from schedular.schedule.models import Task
from typing import Dict

User = get_user_model()


class TaskService:
    def __init__(self, user: User, data: Dict[str, any] | None = None, id: int | None = None) -> None:
        self.user = user
        self.data = data
        self.id = id

    def create_task(self) -> Task:
        return Task.objects.create(owner=self.user, **self.data)

    def update_task(self) -> Task:
        task = self.get_task()

        for key, value in self.data.items():
            setattr(task, key, value)
        task.save()
        return task

    def delete_task(self) -> None:
        self.get_task().delete()

    def get_task(self) -> Task:
        if self.user.is_staff or self.user.is_superuser:
            return get_object_or_404(Task, id=self.id)
        else:
            return get_object_or_404(Task, owner=self.user, id=self.id)
