from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, unique = True)




class Employee(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, unique = True)





class Tasks(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.TextField(max_length=2000)
    descriptions = models.TextField(max_length=2000)
    publish = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    time_to_send = models.DateTimeField(auto_now_add=True)
    preTask = models.TextField(max_length=100,blank=True)

