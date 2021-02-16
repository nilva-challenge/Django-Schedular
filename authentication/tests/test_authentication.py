from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.models import Member


class AuthenticationTest(TestCase):
    def setUp(self):
        self.email = 'authTest@example.com'
        self.username = 'authTest_username'
        self.password = 'authTest_password'
        self.first_name = 'authTest_first_name'
        self.last_name = 'authTest_last_name'
        self.member = Member.objects.create_user(email=self.email,
                                                 username=self.username,
                                                 password=self.password,
                                                 first_name=self.first_name,
                                                 last_name=self.last_name)
        self.data = {
            'username': self.username,
            'password': self.password
        }

    def test_login(self):
        client = APIClient()
        response = client.post('/api/v1.0/auth/login/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_wrong_username(self):
        self.data['username'] = 'wrong'
        client = APIClient()
        response = client.post('/api/v1.0/auth/login/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_wrong_password(self):
        self.data['password'] = 'wrong'
        client = APIClient()
        response = client.post('/api/v1.0/auth/login/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        client = APIClient()
        response1 = client.post('/api/v1.0/auth/login/', self.data, format='json')
        refresh = {"refresh": str(response1.data['refresh'])}
        response = client.post('/api/v1.0/auth/token/refresh/', refresh, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token_wrong(self):
        client = APIClient()
        refresh = {"refresh": "wrong"}
        response = client.post('/api/v1.0/auth/token/refresh/', refresh, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
