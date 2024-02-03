from django.db import models
from users.models import CustomUser
from datetime import datetime
from collections import defaultdict

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time_to_send = models.DateTimeField()
    precondition_tasks = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.title


class CeleryJobInfo(models.Model):
  DONE = 'done'
  PENDING = 'pend'
  FAILED = 'failed'

  TASK_STATES = [
      (DONE, 'Done'),
      (PENDING, 'Pending'),
      (FAILED, 'Failed'),
  ]
  
  state = models.CharField(max_length=10, choices=TASK_STATES, default=PENDING)
  task = models.ForeignKey(Task, on_delete=models.CASCADE)
  celery_job_id = models.CharField(max_length=255, null=True, blank=True, default='')


class TaskValidator:
    def __init__(self, task):
        self.task = task

    def is_valid(self):
        if not self.task.precondition_tasks:
            return True
        if not self.validate_time_to_send(self.task):
            return False
        return True

    def validate_time_to_send(self, task):
        for pre_task in task.precondition_tasks.all():
            if task.time_to_send <= pre_task.time_to_send:
                return False
        return True
