from schedular.schedule.services import (
    TaskService,
    SendEmailForTaskOwnerService,
    ValidateTaskService
)

from schedular.schedule.email import MockEmailService
from django.contrib.auth import get_user_model
from django.core.exceptions import BadRequest
from schedular.schedule.models import Task
from datetime import datetime, timedelta
from django.test import TestCase
from django.http import Http404

User = get_user_model()


class TaskServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user', is_superuser=False)
        self.task_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'time_to_send': datetime.now() + timedelta(days=1),
            'precondition_tasks': None
        }

    def test_create_task(self):
        task_service = TaskService(user=self.user, data=self.task_data)
        created_task = task_service.create_task()

        self.assertIsInstance(created_task, Task)
        self.assertEqual(created_task.title, self.task_data['title'])

        created_task.delete()

    def test_update_task(self):
        initial_task = Task.objects.create(owner=self.user, **self.task_data)

        updated_task_data = {
            'title': 'Updated Task',
            'description': 'This task has been updated',
            'precondition_tasks': None,
        }

        task_service = TaskService(user=self.user, data=updated_task_data)
        updated_task = task_service.update_task(id=initial_task.id)

        self.assertIsInstance(updated_task, Task)
        self.assertEqual(updated_task.title, updated_task_data['title'])
        self.assertEqual(updated_task.description, updated_task_data['description'])

        updated_task.delete()

    def test_delete_task(self):
        task_to_delete = Task.objects.create(owner=self.user, **self.task_data)

        task_service = TaskService(user=self.user, data=self.task_data)
        task_service.delete_task(id=task_to_delete.id)

        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=task_to_delete.id)

    def test_get_task(self):
        task_to_retrieve = Task.objects.create(owner=self.user, **self.task_data)

        task_service = TaskService(user=self.user, data=self.task_data)
        retrieved_task = task_service.get_task(id=task_to_retrieve.id)

        self.assertIsInstance(retrieved_task, Task)
        self.assertEqual(retrieved_task.id, task_to_retrieve.id)

        task_to_retrieve.delete()


class SendEmailForTaskOwnerServiceTest(TestCase):

    def setUp(self):
        self.email_service = MockEmailService()

        self.user_data = {'username': 'test_user', 'email': 'test_user@example.com', 'password': 'password'}

        self.user = User.objects.create_user(**self.user_data)

        self.task_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'owner': self.user,
            'time_to_send': datetime.now() + timedelta(days=1),
            'precondition_tasks': None,

        }

    def test_send_email_and_change_task_status_success(self):
        task = Task.objects.create(**self.task_data)

        service = SendEmailForTaskOwnerService(email_service=self.email_service)
        service.send_email_and_change_task_status(task_id=task.id)
        task.refresh_from_db()

        self.assertTrue(task.sent)

    def test_send_email_and_change_task_status_task_not_found(self):
        service = SendEmailForTaskOwnerService(email_service=self.email_service)

        with self.assertRaises(Http404):
            service.send_email_and_change_task_status(task_id=999)

    def test_check_preconditions_tasks_success(self):
        task = Task.objects.create(**self.task_data)
        service = SendEmailForTaskOwnerService(email_service=self.email_service)
        service.check_preconditions_tasks(task)


class TestValidateTaskService(TestCase):

    def setUp(self):
        self.sample_user = User.objects.create(username='test_user', is_superuser=False)

    def test_check_if_tasks_send_time_is_correct(self):
        task1 = Task.objects.create(title='Task1', description='Description1', owner=self.sample_user, time_to_send=datetime.now())
        task2 = Task.objects.create(title='Task2', description='Description2', owner=self.sample_user, time_to_send=datetime.now() + timedelta(days=1))

        tasks = [task1, task2]

        validate_service = ValidateTaskService(user=self.sample_user, ids=[task1.id, task2.id])
        result = validate_service.check_if_tasks_send_time_is_correct(tasks)

        self.assertEqual(result, [task1.id, task2.id])

        task3 = Task.objects.create(title='Task3', description='Description3', owner=self.sample_user, time_to_send=datetime.now() + timedelta(days=2))
        task3.precondition_tasks = task1
        task3.save()

        tasks = [task1, task2, task3]

        validate_service = ValidateTaskService(user=self.sample_user, ids=[task1.id, task2.id, task3.id])
        result = validate_service.check_if_tasks_send_time_is_correct(tasks)

        self.assertEqual(result, [task1.id, task2.id, task3.id])

    def test_get_tasks(self):
        superuser = User.objects.create(username='superuser', is_superuser=True)
        task1 = Task.objects.create(title='Task1', description='Description1', owner=superuser, time_to_send=datetime.now())
        task2 = Task.objects.create(title='Task2', description='Description2', owner=superuser, time_to_send=datetime.now() + timedelta(days=1))

        validate_service_superuser = ValidateTaskService(user=superuser, ids=[task1.id, task2.id])
        result_superuser = validate_service_superuser.get_tasks()

        self.assertEqual(list(result_superuser), [task1, task2])

        task3 = Task.objects.create(title='Task3', description='Description3', owner=self.sample_user, time_to_send=datetime.now() + timedelta(days=2))
        task4 = Task.objects.create(title='Task4', description='Description4', owner=self.sample_user, time_to_send=datetime.now() + timedelta(days=3))

        validate_service_user = ValidateTaskService(user=self.sample_user, ids=[task3.id, task4.id])
        result_user = validate_service_user.get_tasks()

        self.assertEqual(list(result_user), [task3, task4])

    def test_get_tasks_invalid_input(self):
        single_task = Task.objects.create(title='SingleTask', description='SingleTaskDesc', owner=self.sample_user, time_to_send=datetime.now())

        with self.assertRaises(BadRequest):
            validate_service_single_task = ValidateTaskService(user=self.sample_user, ids=[single_task.id])
            validate_service_single_task.get_tasks()
