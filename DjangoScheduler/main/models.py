from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from DjangoScheduler.controller import Controller


class CustomUser(AbstractUser):
    roleChoices = (("A", "admin"), ('N', "normal"))
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

    def __str__(self):
        return '{}-{}-{}'.format(self.title,self.owner.first_name,self.timeToSend)


    def save(self, *args, **kwargs):

        controller = Controller()

        print(self.timeToSend)

        if self.pk:
            controller.updateTask(self)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
            controller.scheduleTask(self)
