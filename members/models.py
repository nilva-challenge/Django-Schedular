from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.auth.models import AbstractUser


class Member(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class TaskPermission(models.TextChoices):
    VIEW_TASK = "view_task", "Can view tasks"
    CHANGE_TASK = "change_task", "Can change tasks"
    DELETE_TASK = "delete_task", "Can delete tasks"
