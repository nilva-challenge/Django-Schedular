from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from tasks.models import Task
from django.utils import timezone

class TaskViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        CustomUser = get_user_model()
        self.user = CustomUser(username='testuser', email='testuser@example.com')
        self.user.set_password('testpass')
        self.user.save()

        self.task = Task.objects.create(
            title='Test Task',
            description='Test Desc',
            owner=self.user,
            time_to_send=timezone.now() + timezone.timedelta(days=1)
        )

        self.client.force_authenticate(user=self.user)

    def test_get_task_list(self):
        url = reverse('task-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_task(self):
        url = reverse('task-list-create')
        data = {
            'title': 'New Task', 
            'description': 'New Desc', 
            'time_to_send': timezone.now() + timezone.timedelta(days=1)
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_get_task_detail(self):
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')

    def test_update_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        data = {
            'title': 'Updated Task', 
            'description': self.task.description, 
            'time_to_send': self.task.time_to_send
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(updated_task.title, 'Updated Task')

    def test_delete_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())


    # Admin Scenario Tests

    def test_admin_access_to_all_tasks(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('task-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming there are multiple tasks in the database, admin should see all
        self.assertTrue(len(response.data) > 1)

    def test_admin_update_any_task(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        data = {'title': 'Admin Updated Task'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
