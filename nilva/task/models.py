from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    tile=models.CharField(max_length=128)
    description=models.TextField()
    owner=models.OneToOneField(User,on_delete=models.CASCADE)
    time_to_send_field=models.DateTimeField()

    def __str__(self) -> str:
        return self.tile