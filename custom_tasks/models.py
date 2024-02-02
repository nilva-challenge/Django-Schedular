from django.db import models
from users.models import CustomUser
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
