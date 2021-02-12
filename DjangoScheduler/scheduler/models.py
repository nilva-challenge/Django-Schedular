from django.db import models

# Create your models here.


class Task(models.Model):
    uuid = models.CharField(max_length=36)
    data = models.ForeignKey(to='main.Task', on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.data.title)