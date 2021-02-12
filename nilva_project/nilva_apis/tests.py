from django.test import TestCase , Client
from django.urls import reverse
from nilva_accounts.models import User
from nilva_accounts.services import UserService


class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = Client()
        user_service = UserService()
        user = User(username="pezhman",email="pezhman@gmail.com",first_name="pezhman",last_name="morsali")
        user_service.hash_password(user,"123456")
        

    def test_valid_data_register(self):
        response = self.client.post(reverse('api:user_register'),data={
            "username" : "erfanmorsali",
            "first_name" : "erfan",
            "last_name" : "morsali" , 
            "email" : "erfanmorsali@gmail.com",
            "password" : "123456"
        })
        self.assertEqual(response.status_code , 201)
        self.assertEqual(User.objects.count(),2)

    def test_invalid_data_register(self):
        response = self.client.post(reverse('api:user_register'),data={
            "username" : "pezhman",
            "email" : "pezhman@gmail.com",
            "password" : "2121213213"
        })
        self.assertEqual(response.status_code , 400)

    def test_valid_data_login(self):
        response = self.client.post(reverse("token_obtain_pair"),data={
            "username" : "pezhman",
            "password" : "123456"
        })
        self.assertEqual(response.status_code,200)
    
    def test_invalid_data_login(self):
        response = self.client.post(reverse("token_obtain_pair"),data={
            "username" : "asdsadasdsad",
            "password" : "2a1sd32a1d32a1sd"
        })
        self.assertEqual(response.status_code,401)