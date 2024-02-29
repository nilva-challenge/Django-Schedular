# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    permissions = models.CharField(max_length=10, choices=[
                                   ('admin', 'Admin'), ('normal', 'Normal')])

    def __str__(self):
        return self.username


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    time_to_send = models.DateTimeField()
    pre_tasks = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return self.title
