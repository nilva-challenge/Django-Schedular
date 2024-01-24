from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.exceptions import BadRequest
from schedular.schedule.models import Task
from django.db.models import QuerySet
from django.http import Http404
from .email import EmailService
from typing import Dict

User = get_user_model()


class TaskService:
    def __init__(self, user: User, data: Dict[str, any] | None = None, id: int | None = None) -> None:
        self.user = user
        self.data = data
        self.id = id

    def create_task(self) -> Task:
        pre_task = self.data.pop('precondition_tasks')
        task = Task.objects.create(owner=self.user, **self.data)
        task.precondition_tasks.set(pre_task)
        return task

    def update_task(self) -> Task:
        pre_task = self.data.pop('precondition_tasks')
        task = self.get_task()

        for key, value in self.data.items():
            setattr(task, key, value)

        if pre_task is not None:
            task.precondition_tasks.set(pre_task)

        task.save()
        return task

    def delete_task(self) -> None:
        self.get_task().delete()

    def get_task(self) -> Task:
        if self.user.is_superuser:
            return get_object_or_404(Task, id=self.id)
        else:
            return get_object_or_404(Task, owner=self.user, id=self.id)


class SendEmailForTaskOwnerService:
    def __init__(self, email_service: EmailService) -> None:
        self.email_service = email_service

    def send_email_and_change_task_status(self, task_id: int) -> None:
        task = self.get_task(task_id=task_id)
        task.sent = True
        task.save()

        self.email_service.send_email(
            task.title,
            task.description,
            "amirjas8177@gmail.com",
            [task.owner.email]
        )

    def get_task(self, task_id: int) -> Task:
        try:
            task = Task.objects.select_related('owner').prefetch_related('precondition_tasks').get(id=task_id)
        except Task.DoesNotExist:
            raise Http404
        self.check_preconditions_tasks(task.precondition_tasks)
        return task

    @staticmethod
    def check_preconditions_tasks(pre_tasks: QuerySet[Task]) -> None:
        for task in pre_tasks.all():
            if task.sent is False:
                raise BadRequest('The prerequisites for this task have not been met')
