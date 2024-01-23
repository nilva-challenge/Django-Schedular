from django.db import models
from django.contrib.auth import get_user_model
from schedular.common.models import BaseModel

User = get_user_model()


class Task(BaseModel, models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner_tasks'
    )
    time_to_send = models.DateTimeField()
    precondition_tasks = models.ManyToManyField(
        'self', blank=True,
        related_name='pre_tasks'
    )
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner.username}-{self.title}'
