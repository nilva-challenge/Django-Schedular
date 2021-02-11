from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group


class CustomUser(AbstractUser):
    roleChoices = (("A", 'admin'), ('N', 'normal'))
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    role = models.CharField(max_length=2, choices=roleChoices, default='N')
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)


class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timeToSend = models.DateTimeField()

    def save(self, *args, **kwargs):
        print('creating/saving object with args ', args, kwargs)
        if self.pk:
            print('record exists, updtating...new name is: ', self.title)
        else:
            print('newly saving record...')

        super().save(*args, **kwargs)

    def update(self, *args, **kwargs):
        print('updating task with args: ', args, kwargs)
        # super().update(*args, **kwargs)
