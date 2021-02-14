from django.contrib.auth.models import AbstractUser
from django.db import models


class Member(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=False, unique=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
