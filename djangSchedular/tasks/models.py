from django.contrib.admin.sites import site
from django.db import models
import uuid

from django.db.models.deletion import PROTECT
from users.models import Profile


class Task(models.Model):
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    timeToSend = models.DateTimeField()
    owner= models.ForeignKey(Profile, null=True , blank=True ,on_delete=models.SET_NULL)
    pre_tasks = models.ManyToManyField('Task',blank=True)
    def __str__(self):
        return self.title
