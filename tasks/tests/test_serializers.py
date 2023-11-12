from django.test import TestCase
from django.contrib.auth import get_user_model
from tasks.models import Task
from tasks.api.serializers import TaskSerializer
from django.utils import timezone

class TaskSerializerTest(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create(**self.user_data)
        self.task_data = {
            'title': 'Sample Task',
            'description': 'Sample Description',
            'owner': self.user,
            'time_to_send': timezone.now()
        }
        self.task = Task.objects.create(**self.task_data)

    def test_valid_serializer(self):
        serializer = TaskSerializer(instance=self.task)
        self.assertEqual(serializer.data, self.task_data)

    def test_serializer_create(self):
        task_data = {
            'title': 'New Task',
            'description': 'New Description',
            'owner': self.user.id,
            'time_to_send': timezone.now()
        }
        serializer = TaskSerializer(data=task_data)
        self.assertTrue(serializer.is_valid())
        task = serializer.save()
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(task.title, 'New Task')

    def test_serializer_update(self):
        update_data = {'title': 'Updated Task'}
        serializer = TaskSerializer(instance=self.task, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        task = serializer.save()
        self.assertEqual(task.title, 'Updated Task')

    def test_invalid_serializer(self):
        invalid_data = self.task_data.copy()
        invalid_data['title'] = ''  # Assuming title is required
        serializer = TaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
