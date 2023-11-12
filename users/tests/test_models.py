from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from users.models import CustomUser

class CustomUserModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', username='testuser', password='123')

    def test_create_user(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.username, 'testuser')

    def test_email_uniqueness(self):
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(email='test@example.com', username='testuser2', password='123')

    def test_string_representation(self):
        self.assertEqual(str(self.user), self.user.email)

    def test_email_login(self):
        user = CustomUser.objects.get(email='test@example.com')
        self.assertEqual(user.username, 'testuser')
