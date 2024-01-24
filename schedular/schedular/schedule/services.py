from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.exceptions import BadRequest
from schedular.schedule.models import Task
from django.db.models import QuerySet
from typing import Dict, List, Union
from django.http import Http404
from .email import EmailService

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
        task = Task.objects.create(owner=self.user, **self.data)
        return task

    def update_task(self, id: int) -> Task:
        task = self.get_task(id=id)

        for key, value in self.data.items():
            setattr(task, key, value)

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
        self.check_preconditions_tasks(task)
        return task

    @staticmethod
    def check_preconditions_tasks(pre_tasks: Task) -> None:
        pre_tasks = pre_tasks.pre_tasks.all()
        for pre_task in pre_tasks:
            if pre_task.sent is False:
                raise BadRequest('The prerequisites for this task have not been met')


class ValidateTaskService:
    """
      A service class for validating tasks based on their time-to-send properties and preconditions.

      Attributes:
          user (User): The user for whom the validation is performed.
          ids (List[int]): List of task IDs to be validated.
    """

    def __init__(self, user: User, ids: List[int]) -> None:
        self.user = user
        self.ids = ids

    @staticmethod
    def check_if_tasks_send_time_is_correct(tasks: QuerySet[Task]) -> Union[List[int], str]:
        can_execute = []

        for task in tasks:

            if not task.precondition_tasks:
                can_execute.append(task.id)

            if task.precondition_tasks:
                pre_task = task.precondition_tasks

                if pre_task.time_to_send >= task.time_to_send:
                    return f"{pre_task.title} run before {task.title} and it's impossible to run because {task.title} is dependese on {pre_task.title}"

                if pre_task.time_to_send <= task.time_to_send:
                    can_execute.append(task.id)

        return can_execute

    def get_tasks(self) -> QuerySet[Task]:
        if self.user.is_superuser:
            tasks = Task.objects.prefetch_related('precondition_tasks').filter(id__in=self.ids)
        else:
            tasks = Task.objects.prefetch_related('precondition_tasks').filter(owner=self.user, id__in=self.ids)

        if len(tasks) <= 1:
            raise BadRequest('at least tow task need for validation')
        return tasks.order_by('time_to_send')
