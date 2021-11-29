from django.http import response
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import User
from rest_framework import status
from rest_framework.authtoken.models import Token


class UsersTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            password='password', email='test@gmail.com',
            username='test', first_name='test', last_name='test',
            permissions='1', is_staff=True, is_superuser=True)
        self.create_url = reverse('taskmanager:signup')

    def testSmokeTest(self):
        self.assertEquals(1, 1)
        
    def test_create_user(self):
        data = {
            'username':'exmaple',
            'email': 'example@example.com',
            'password': 'somepassword',
            'first_name':'exmaple1',
            'last_name':'example2',
            'permissions':'2'
        }
        response = self.client.post(self.create_url, data, format='json')
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode('ascii')[2:-2], token.key)


    def test_create_user_with_no_password(self):
        data = {
            'username': 'exmaple',
            'email': 'example@example.com',
            'password': '',
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_too_long_username(self):
        data = {
            'username': 'example'*30,
            'email': 'example@example.com',
            'password': 'somepassword'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        data = {
            'username': '',
            'email': 'example@example.com',
            'password': 'somepassword'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_pre_existing_username(self):
        data = {
            'username': 'test',
            'email': 'user@example.com',
            'password': 'testuser'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_pre_exisging_email(self):
        data = {
            'username': 'testuser2',
            'email': 'test@gmail.com',
            'password': 'testuser',
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        data = {
            'username': 'foobarbaz',
            'email': 'testing',
            'password': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        data = {
            'username': 'foobar',
            'email': '',
            'password': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)
