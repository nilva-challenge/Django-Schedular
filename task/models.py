from django.db import models
from django.conf import settings




class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_to_send = models.DateTimeField()
    pre_task = models.ForeignKey('self', null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.title

