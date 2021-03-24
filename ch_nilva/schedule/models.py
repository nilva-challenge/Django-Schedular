from django.db import models
from account.models import User


class Task(models.Model):
    title = models.CharField(max_length=50, blank=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    description = models.CharField(max_length=150, blank=True)
    time_to_send = models.DateTimeField(blank=False, )

    class Meta:
        db_table = 'tasks'
