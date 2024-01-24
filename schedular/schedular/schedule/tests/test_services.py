from schedular.schedule.services import TaskService, SendEmailForTaskOwnerService
from schedular.schedule.email import MockEmailService
from django.contrib.auth import get_user_model
from schedular.schedule.models import Task
from datetime import datetime, timedelta
from django.test import TestCase
from django.http import Http404

User = get_user_model()


class TaskServiceTest(TestCase):

    def setUp(self):
        # Create a sample user and task data for testing
        self.user = User.objects.create(username='test_user', is_superuser=False)
        self.task_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'time_to_send': datetime.now() + timedelta(days=1),
            'precondition_tasks': [],
        }

    def test_create_task(self):
        task_service = TaskService(user=self.user, data=self.task_data)
        created_task = task_service.create_task()

        # Verify that the task was created successfully
        self.assertIsInstance(created_task, Task)
        self.assertEqual(created_task.title, self.task_data['title'])

        # Cleanup: Delete the created task
        created_task.delete()

    def test_update_task(self):
        preconditions = self.task_data.pop('precondition_tasks')
        initial_task = Task.objects.create(owner=self.user, **self.task_data)
        initial_task.precondition_tasks.set(preconditions), initial_task.save()

        updated_task_data = {
            'title': 'Updated Task',
            'description': 'This task has been updated',
            'precondition_tasks': [],
        }

        task_service = TaskService(user=self.user, data=updated_task_data)
        updated_task = task_service.update_task(id=initial_task.id)

        self.assertIsInstance(updated_task, Task)
        self.assertEqual(updated_task.title, updated_task_data['title'])
        self.assertEqual(updated_task.description, updated_task_data['description'])

        updated_task.delete()

    def test_delete_task(self):
        preconditions = self.task_data.pop('precondition_tasks')
        task_to_delete = Task.objects.create(owner=self.user, **self.task_data)
        task_to_delete.precondition_tasks.set(preconditions), task_to_delete.save()

        task_service = TaskService(user=self.user, data=self.task_data)
        task_service.delete_task(id=task_to_delete.id)

        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=task_to_delete.id)

    def test_get_task(self):
        preconditions = self.task_data.pop('precondition_tasks')
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
            'precondition_tasks': [],

        }

    def test_send_email_and_change_task_status_success(self):
        precondition = self.task_data.pop('precondition_tasks')
        task = Task.objects.create(**self.task_data)
        task.precondition_tasks.set(precondition)

        service = SendEmailForTaskOwnerService(email_service=self.email_service)
        service.send_email_and_change_task_status(task_id=task.id)
        task.refresh_from_db()

        self.assertTrue(task.sent)

    def test_send_email_and_change_task_status_task_not_found(self):
        service = SendEmailForTaskOwnerService(email_service=self.email_service)

        with self.assertRaises(Http404):
            service.send_email_and_change_task_status(task_id=999)

    def test_check_preconditions_tasks_success(self):
        precondition = self.task_data.pop('precondition_tasks')

        pre_task = Task.objects.create(**self.task_data)
        task = Task.objects.create(**self.task_data)

        pre_task.precondition_tasks.set(precondition), pre_task.save()
        task.precondition_tasks.set(precondition), task.save()

        service = SendEmailForTaskOwnerService(email_service=self.email_service)

        service.check_preconditions_tasks(task.precondition_tasks.all())
