from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import User


class AuthenticationTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(email='test1@gmail.com',
                                              username='test1',
                                              password="test123",
                                              first_name="test1",
                                              last_name='test1',
                                              is_admin=True)
        self.data = {
            'username': 'test1',
            'password': 'test123'
        }

    def test_login(self):
        client = APIClient()
        response = client.post('/api/auth/login', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_wrong_username(self):
        self.data['username'] = 'test55'
        client = APIClient()
        response = client.post('/api/auth/login', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_wrong_password(self):
        self.data['password'] = 'test12345'
        client = APIClient()
        response = client.post('/api/auth/login', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_without_password(self):
        self.data = {'username': 'test1'}
        client = APIClient()
        response = client.post('/api/auth/login', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_without_username(self):
        self.data = {'password': 'test123'}
        client = APIClient()
        response = client.post('/api/auth/login', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token(self):
        client = APIClient()
        response1 = client.post('/api/auth/login', self.data, format='json')
        refresh = {"refresh": str(response1.data['refresh'])}
        response = client.post('/api/auth/refresh/token', refresh, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
