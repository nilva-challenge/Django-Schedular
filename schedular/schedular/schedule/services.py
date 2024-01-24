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
    """
        A service class for managing tasks related operations.

        Args:
            user: The user associated with the task operation.
            data: Optional. Data to be used for task creation or update.
            id: Optional. ID of the task to be operated upon.

        Attributes:
            user: The user associated with the task operation.
            data: Data to be used for task creation or update.
            id: ID of the task to be operated upon.
    """

    def __init__(self, user: User, data: Dict[str, any]) -> None:
        self.user = user
        self.data = data
        self.id = id

    def create_task(self) -> Task:
        pre_task = self.data.pop('precondition_tasks')
        task = Task.objects.create(owner=self.user, **self.data)
        task.precondition_tasks.set(pre_task)
        return task

    def update_task(self, id: int) -> Task:
        pre_task = self.data.pop('precondition_tasks')
        task = self.get_task(id=id)

        for key, value in self.data.items():
            setattr(task, key, value)

        if pre_task is not None:
            task.precondition_tasks.set(pre_task)

        task.save()
        return task

    def delete_task(self, id: int) -> None:
        self.get_task(id=id).delete()

    def get_task(self, id: int) -> Task:
        if self.user.is_superuser:
            return get_object_or_404(Task, id=id)
        else:
            return get_object_or_404(Task, owner=self.user, id=id)


class SendEmailForTaskOwnerService:
    """
        Service class for sending emails to the owner of a task and updating the task status.

        Args:
            email_service (EmailService): An instance of the EmailService used for sending emails.

        Attributes:
            email_service (EmailService): The EmailService instance.
    """

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
