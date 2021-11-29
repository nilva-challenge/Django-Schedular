from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = ((1, 'Admin'), (2, 'Normal'))
    email = models.EmailField(max_length=50, null=False, unique=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    permissions = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=False)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username
    


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    time_to_send = models.DateTimeField()
    precondition_tasks = models.ManyToManyField('self', blank=True)
    
    def __str__(self):
        return self.title
    
