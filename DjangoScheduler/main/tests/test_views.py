import json
import re
from operator import add
from unittest import mock
from unittest.mock import patch
from django.contrib.auth.models import User, Permission, Group

from django.contrib.auth import authenticate, login
from django.urls import reverse
from datetime import datetime
from rest_framework import status
from main.models import *
from rest_framework.test import APITestCase
from django.contrib.auth.hashers import make_password


class TestViews(APITestCase):

    @classmethod
    def setUpTestData(cls):

        cls.username = "dummyUsermane"
        cls.password = "dummyPassword"
        cls.normalUsername = "nornalUsername"
        cls.normalEmail = "normalEmail@mail.com"
        cls.firstName = "dummy"
        cls.lastName = "dummy"
        cls.email = "dummy@dummy.com"

        cls.user1 = CustomUser.objects.create(username=cls.username, password=make_password(cls.password),
                                              email=cls.email, role='A', first_name=cls.firstName,
                                              last_name=cls.lastName)

        cls.user2 = CustomUser.objects.create(username='username2', password=make_password(cls.password),
                                              email='email2@dummy.com', role='A', first_name=cls.firstName,
                                              last_name=cls.lastName)

        cls.normalUser = CustomUser.objects.create(username=cls.normalUsername, password=make_password(cls.password),
                                                   email=cls.normalEmail, role='N', first_name=cls.firstName,
                                                   last_name=cls.lastName)

        cls.taskUser1 = Task.objects.create(title='title', description='des',
                                            owner=cls.user1, timeToSend=datetime.now())

        cls.taskUser2 = Task.objects.create(title='title', description='des',
                                            owner=cls.user2, timeToSend=datetime.now())

        cls.task1NormalUser = Task.objects.create(title='title', description='des',
                                            owner=cls.normalUser, timeToSend=datetime.now())

        cls.task2NormalUser = Task.objects.create(title='title', description='des',
                                            owner=cls.normalUser, timeToSend=datetime.now())

        cls.adminGroup = Group.objects.create(name='admin')
        cls.adminGroup.permissions.set(Permission.objects.all())
        cls.normalGroup = Group.objects.create(name='normal')
        
        taskPermissions = Permission.objects.filter(content_type__app_label='main', content_type__model='task')
        # permissiosn coresponds to view,change permissions 
        cls.normalGroup.permissions.set([taskPermissions[1],taskPermissions[3]])

    def testSmokeTest(self):
        self.assertEquals(1, 1)

    def testLoginUserWithInvalidParametersShouldReturn400(self):
        response = self.client.post(reverse(
            'login'), content_type="Application/json", data=json.dumps({'someDummy': 'hello'}))
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.content)
        self.assertFalse('access' in json.loads(response.content))
        self.assertFalse('refresh' in json.loads(response.content))

    def testLoginUserWithIncorrentCredentialsShouldReturn401(self):
        response = self.client.post(
            reverse('login'), content_type="Application/json", data=json.dumps({'username': 'hello', 'password': 'password'}))
        self.assertEqual(response.status_code, 401)
        self.assertIsNotNone(response.content)
        self.assertFalse('access' in json.loads(response.content))
        self.assertFalse('refresh' in json.loads(response.content))

    def testLoginUserWithCorrentCredentialsShouldReturnToken200(self):
        response = self.client.post(
            reverse('login'), content_type="Application/json", data=json.dumps({"username": self.username,
                                                                                "password": self.password}))

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertTrue('access' in json.loads(response.content))
        self.assertTrue('refresh' in json.loads(response.content))

    def testSignUpUserWithInvalidParametersShouldReturn400(self):
        response = self.client.post(
            reverse('signUp'), content_type="Application/json", data=json.dumps({"username": self.username,
                                                                                 "password": self.password,
                                                                                 }))

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.content)

    def testSignUpUserWithInvalidEmailShouldReturn400(self):

        response = self.client.post(
            reverse('signUp'), content_type="Application/json", data=json.dumps({"username": self.username,
                                                                                 "password": self.password,
                                                                                 "first_name": "first",
                                                                                 "last_name": "last",
                                                                                 "email": "InvalidEmail",
                                                                                 "role": "N"}))

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.content)

    def testSignUpUserWithAlreadyRegisterdUsernameShouldReturn400(self):

        response = self.client.post(
            reverse('signUp'), content_type="Application/json", data=json.dumps({"username": self.username,
                                                                                 "password": self.password,
                                                                                 "first_name": "first",
                                                                                 "last_name": "last",
                                                                                 "email": "valid@valid.com",
                                                                                 "role": "N"}))

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.content)

    def testSignUpUserWithAlreadyRegisterdEmailShouldReturn400(self):

        response = self.client.post(
            reverse('signUp'), content_type="Application/json", data=json.dumps({"username": self.username,
                                                                                 "password": self.password,
                                                                                 "first_name": "first",
                                                                                 "last_name": "last",
                                                                                 "email": self.email,
                                                                                 "role": "N"}))

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.content)

    def testSignUpUserWithValidCrednetialsShouldCreateNewUser201(self):

        response = self.client.post(
            reverse('signUp'), content_type="Application/json", data=json.dumps({"username": "newuser",
                                                                                 "password": self.password,
                                                                                 "first_name": "first",
                                                                                 "last_name": "last",
                                                                                 "email": "self.email@email.com",
                                                                                 "role": "N"}))

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.content)
        self.assertTrue('token' in json.loads(response.content))

    def testViewTaskWithUnAuthenticatedUserShouldReturn401(self):
        response = self.client.get(
            reverse('tasks'), content_type="Application/json")

        self.assertEqual(response.status_code, 401)

    def testViewTaskWithInvalidTokenShouldReturn401(self):
        headers = {"Authorization": "Bearer eyJ0eXAiOidJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjEzMDg4NjUwLCJqdGkiOiJhYmZjYjBlOWFlNTU0OTkzOGI2YzVmMWEwMzQwNTMwMSIsInVzZXJfaWQiOjV9.bGQzh4JO5pRD9W8U1UPJBO2wTPeXogVtTKGmM_UvmyY"}
        response = self.client.get(
            reverse('tasks'), headers=headers, content_type="Application/json")

        self.assertEqual(response.status_code, 401)

    def testViewTaskWithValidTokenForAdminUserShouldReturn200(self):
        tokenResponse = self.client.post(
            reverse('login'), content_type="Application/json", data=json.dumps({"username": self.username, "password": self.password}))
        token = json.loads(tokenResponse.content)['access']
        headers = {"Authorization": "Bearer "+token}
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer {}'.format(token))

        response = self.client.get(
            reverse('tasks'), content_type="Application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)

    def testViewTaskWithValidTokenForNonAdminUserShouldReturn200OnlyOwnTasks(self):
        tokenResponse = self.client.post(
            reverse('login'), content_type="Application/json", data=json.dumps({"username": self.normalUsername, "password": self.password}))
        token = json.loads(tokenResponse.content)['access']
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer {}'.format(token))

        response = self.client.get(
            reverse('tasks'), content_type="Application/json")
        self.assertEqual(response.status_code, 200)

        # checking if owner of taks points to only this user
        data = json.loads(response.content)
        for item in data:
            self.assertEquals(item['owner'],self.normalUser.pk)

