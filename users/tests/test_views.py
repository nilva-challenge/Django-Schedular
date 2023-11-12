from rest_framework.test import APIClient, APITestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from users.models import CustomUser
from django.contrib.auth import get_user_model

class RegistrationAPIViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse('register')

    def test_registration_success(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.registration_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_failure(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            # Omitting password to simulate invalid data
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.registration_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


CustomUser = get_user_model()  # Get the custom user model


class LoginAPITestCase(TestCase):
    def setUp(self):
        # Create a custom user for testing
        self.user = CustomUser(email='test@example.com')
        self.user.set_password('password123')
        self.user.save()

    def test_login_successful(self):
        client = APIClient()
        data = {'email': 'test@example.com', 'password': 'password123'}
        response = client.post('/users/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Login successful')

    def test_login_invalid_credentials(self):
        client = APIClient()
        data = {'email': 'test@example.com', 'password': 'wrongpassword'}
        response = client.post('/users/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Invalid credentials')
