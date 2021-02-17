from django.db import models


from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=150, blank=False)
    description = models.CharField(max_length=300, blank=True)
    owner = models.ForeignKey('users.Member', on_delete=models.CASCADE, related_name='Tasks')
    time_to_send = models.DateTimeField(blank=False)

    def __str__(self):
        return self.title
