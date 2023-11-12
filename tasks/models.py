from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from .tasks import send_task_email

CustomUser = get_user_model()

# Task model
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    time_to_send = models.DateTimeField()
    pre_tasks = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='dependent_tasks')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Call the real save() method
        super(Task, self).save(*args, **kwargs)
        
        # Schedule the Celery task only if the time_to_send is in the future
        if self.time_to_send and self.time_to_send > now():
            send_task_email.apply_async((self.id,), eta=self.time_to_send)
