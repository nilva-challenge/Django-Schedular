from django.db import models
from members.models import Member


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(Member, on_delete=models.CASCADE)
    time_to_send = models.DateTimeField()
    precondition_tasks = models.ManyToManyField("Task", blank=True)

    def __str__(self):
        return self.title
