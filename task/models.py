from django.db import models
from django.contrib.auth import get_user_model as User

class Task(models.Model):
    title=models.CharField(max_length=250)
    descriptions=models.TextField()
    owner=models.ForeignKey(User(),on_delete=models.CASCADE)
    time_to_send=models.TimeField()
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title