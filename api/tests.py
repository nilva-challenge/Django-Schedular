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
from django.contrib.auth.models import User
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

        cls.user1 = User.objects.create(
            username=cls.username, password=make_password(cls.password), email=cls.email
        )

        cls.user2 = User.objects.create(
            username="username2",
            password=make_password(cls.password),
            email="email2@dummy.com",
        )

        cls.normalUser = User.objects.create(
            username=cls.normalUsername,
            password=make_password(cls.password),
            email=cls.normalEmail,
        )

    def testSmokeTest(self):
        self.assertEquals(1, 1)

    def testLoginUserWithInvalidParametersShouldReturn400(self):
        response = self.client.post(
            reverse("loginAPI"),
            content_type="Application/json",
            data=json.dumps({"someDummy": "hello"}),
        )
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.content)
        self.assertFalse("access" in json.loads(response.content))
        self.assertFalse("refresh" in json.loads(response.content))

    def testLoginUserWithIncorrentCredentialsShouldReturn401(self):
        response = self.client.post(
            reverse("loginAPI"),
            content_type="Application/json",
            data=json.dumps({"username": "hello", "password": "password"}),
        )
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.content)
        self.assertFalse("access" in json.loads(response.content))
        self.assertFalse("refresh" in json.loads(response.content))

    def testLoginUserWithCorrentCredentialsShouldReturnToken200(self):
        response = self.client.post(
            reverse("loginAPI"),
            content_type="Application/json",
            data=json.dumps({"username": self.username, "password": self.password}),
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertTrue("token" in json.loads(response.content))

    def testSignUpUserWithInvalidParametersShouldReturn400(self):
        response = self.client.post(
            reverse("registerAPI"),
            content_type="Application/json",
            data=json.dumps(
                {
                    "username": self.username,
                    "password": self.password,
                }
            ),
        )

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.content)

    def testSignUpUserWithInvalidEmailShouldReturn400(self):

        response = self.client.post(
            reverse("registerAPI"),
            content_type="Application/json",
            data=json.dumps(
                {
                    "username": self.username,
                    "password": self.password,
                    "email": "InvalidEmail",
                }
            ),
        )

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.content)

    def testSignUpUserWithAlreadyRegisterdUsernameShouldReturn400(self):

        response = self.client.post(
            reverse("registerAPI"),
            content_type="Application/json",
            data=json.dumps(
                {
                    "username": self.username,
                    "password": self.password,
                    "email": "valid@valid.com",
                }
            ),
        )

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.content)

    def testSignUpUserWithAlreadyRegisterdEmailShouldReturn400(self):

        response = self.client.post(
            reverse("registerAPI"),
            content_type="Application/json",
            data=json.dumps(
                {
                    "username": self.username,
                    "password": self.password,
                    "email": self.email,
                }
            ),
        )

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.content)

    def testSignUpUserWithValidCrednetialsShouldCreateNewUser201(self):

        response = self.client.post(
            reverse("registerAPI"),
            content_type="Application/json",
            data=json.dumps(
                {
                    "username": "newuser",
                    "password": self.password,
                    "email": "self.email@email.com",
                }
            ),
        )

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.content)
        # self.assertTrue('token' in json.loads(response.content))
