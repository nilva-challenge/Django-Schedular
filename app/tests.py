from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task
from .serializers import *

User = get_user_model()


class TaskListCreateViewTests(APITestCase):
    def create_authenticated_user(self):
        """
        Helper method to create an authenticated user.
        """
        user = User.objects.create_user(
            username='testuser',
            password='testpassword1234',
            email='testuser@example.com'
        )
        self.client.force_authenticate(user=user)
        return user

    def setUp(self):
        self.user = self.create_authenticated_user()
        self.task_data = {
            'title': 'Test Task',
            'description': 'Test description',
            'time_to_send': timezone.now(),
        }
        self.url = reverse('task_list_create')

    def test_create_task(self):
        response = self.client.post(self.url, self.task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def test_get_user_tasks(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)


class TaskRetrieveViewTests(APITestCase):
    def create_authenticated_user(self):
        """
        Helper method to create an authenticated user.
        """
        user = User.objects.create_user(
            username='testuser',
            password='testpassword1234',
            email='testuser@example.com'
        )
        self.client.force_authenticate(user=user)
        return user

    def setUp(self):
        self.user = self.create_authenticated_user()
        self.task_data = {
            'title': 'Test Task',
            'description': 'Test description',
            'time_to_send': timezone.now(),
        }
        self.task = Task.objects.create(owner=self.user, **self.task_data)
        self.url = reverse('task_edit', kwargs={'pk': self.task.id})

    def test_retrieve_task(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serialized_data = TaskSerializer(instance=self.task).data
        self.assertEqual(response.data, serialized_data)


class UserListCreateViewTests(APITestCase):
    def create_authenticated_admin(self):
        """
        Helper method to create an authenticated admin user.
        """
        admin = User.objects.create_user(
            username='adminuser',
            password='adminpassword1234',
            email='adminuser@example.com',
            permissions='admin',
        )
        self.client.force_authenticate(user=admin)
        return admin

    def setUp(self):
        self.admin = self.create_authenticated_admin()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword1234',
            'email': 'testuser@example.com',
            'permissions': 'normal',
        }
        self.url = reverse('user_list_create')

    def test_create_user_by_admin(self):
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_get_user_list_by_admin(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        serialized_data = UserSerializer(
            instance=[self.admin], many=True).data
        self.assertEqual(response.data['results'], serialized_data)


class UserRetrieveUpdateDestroyViewTests(APITestCase):
    def create_authenticated_admin(self):
        """
        Helper method to create an authenticated admin user.
        """
        admin = User.objects.create_user(
            username='adminuser',
            password='adminpassword1234',
            email='adminuser@example.com',
            permissions='admin',
        )
        self.client.force_authenticate(user=admin)
        return admin

    def setUp(self):
        self.admin = self.create_authenticated_admin()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword1234',
            'email': 'testuser@example.com'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.url = reverse('user_edit', kwargs={'pk': self.user.id})

    def test_retrieve_user_by_admin(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serialized_data = UserSerializer(instance=self.user).data
        self.assertEqual(response.data, serialized_data)

    def test_update_user_by_admin(self):
        updated_data = {'username': 'newusername',
                        'email': 'newemail@example.com'}
        response = self.client.patch(self.url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, updated_data['username'])
        self.assertEqual(self.user.email, updated_data['email'])

    def test_delete_user_by_admin(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)


class TaskAdminListCreateViewTests(APITestCase):
    def create_authenticated_admin(self):
        admin = User.objects.create_user(
            username='adminuser',
            password='adminpassword1234',
            email='adminuser@example.com',
            permissions='admin'
        )
        self.client.force_authenticate(user=admin)
        return admin

    def setUp(self):
        self.admin = self.create_authenticated_admin()
        self.task_data = {
            'title': 'Test Task',
            'description': 'Test description',
            'time_to_send': timezone.now(),
            'owner': self.admin.id,
        }
        self.url = reverse('admin_task_list_create')

    def test_create_task_by_admin(self):
        response = self.client.post(self.url, self.task_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def test_get_task_list_by_admin(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)


class TaskRetrieveUpdateDestroyViewTests(APITestCase):
    def create_authenticated_admin(self):
        admin = User.objects.create_user(
            username='adminuser',
            password='adminpassword1234',
            email='adminuser@example.com',
            permissions='admin'
        )
        self.client.force_authenticate(user=admin)
        return admin

    def setUp(self):
        self.admin = self.create_authenticated_admin()
        self.task_data = {
            'title': 'Test Task',
            'description': 'Test description',
            'time_to_send': timezone.now(),
            'owner': self.admin,
        }
        self.task = Task.objects.create(**self.task_data)
        self.url = reverse('admin_task_edit', kwargs={
                           'pk': self.task.id})  # Correct URL name

    def test_retrieve_task_by_admin(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serialized_data = TaskAdminSerializer(instance=self.task).data
        self.assertEqual(response.data, serialized_data)

    def test_update_task_by_admin(self):
        updated_data = {'title': 'New Title', 'description': 'New Description'}
        response = self.client.patch(self.url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.task.refresh_from_db()
        self.assertEqual(self.task.title, updated_data['title'])
        self.assertEqual(self.task.description, updated_data['description'])

    def test_delete_task_by_admin(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
