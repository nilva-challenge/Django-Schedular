from django.db import models
from nilva_accounts.models import User
from datetime import datetime , timezone
from django.db.models.signals import pre_save , pre_delete
from .utils import remove_current_task, set_new_task

# Create your models here.


class Todo(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(default=1)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField()
    async_task_id = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.title
    

    def get_time_difference(self):
        now = datetime.now(timezone.utc)
        todo_time = self.date
        difference = todo_time - now
        return difference.total_seconds()


def set_todo_reminder(sender,instance,*args,**kwargs):
    if instance.async_task_id is None:
        task_id = set_new_task(instance.get_time_difference(),instance.owner.email)
        instance.async_task_id = task_id
    else:
        remove_current_task(instance.async_task_id)
        task_id = set_new_task(instance.get_time_difference(),instance.owner.email)
        instance.async_task_id = task_id


def delete_reminder(sender,instance,*args,**kwargs):
    remove_current_task(instance.async_task_id)


pre_save.connect(set_todo_reminder,Todo)
pre_delete.connect(delete_reminder,Todo)