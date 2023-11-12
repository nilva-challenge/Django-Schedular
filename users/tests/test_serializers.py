from django.test import TestCase
from users.models import CustomUser
from users.api.serializers import UserSerializer, LoginSerializer

class UserSerializerTest(TestCase):

    def test_valid_user_creation(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'first_name': 'New',
            'last_name': 'User'
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(CustomUser.objects.get(username='newuser'), user)
        self.assertTrue(user.check_password('newpassword'))

    def test_login_serializer_validation(self):
        data = {'username': 'newuser', 'password': 'newpassword'}
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
