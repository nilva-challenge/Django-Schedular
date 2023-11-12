from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from tasks.models import Task, CustomUser

class TaskModelTest(TestCase):

    def setUp(self):
        # Create a test user manually
        CustomUser = get_user_model()
        self.user = CustomUser(username='testuser', email='testuser@example.com')
        self.user.set_password('12345')
        self.user.save()

        # Create a test task
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            owner=self.user,
            time_to_send=timezone.now()
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertEqual(self.task.owner, self.user)
        self.assertTrue(isinstance(self.task.time_to_send, timezone.datetime))

    def test_task_string_representation(self):
        self.assertEqual(str(self.task), 'Test Task')

    def test_pre_tasks_relationship(self):
        # Create a second task
        pre_task = Task.objects.create(
            title='Pre Task',
            description='Pre Description',
            owner=self.user,
            time_to_send=timezone.now()
        )
        # Add the pre_task as a pre_task of the main task
        self.task.pre_tasks.add(pre_task)
        self.assertIn(pre_task, self.task.pre_tasks.all())
