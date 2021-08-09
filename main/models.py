from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class TaskManager(models.Manager):
    def get_user_tasks(self, user, keyword):
        if keyword == None:
            keyword = ''
        if user.permission == 'A':
            tasks = Task.objects.select_related('owner').all() \
                .filter(title__icontains=keyword)
        else:
            tasks = Task.objects.select_related('owner').filter(owner=user) \
                .filter(title__icontains=keyword)
        return tasks

    def get_task_by_id(self, pk):
        tasks = Task.objects.select_related('owner').get(pk=pk)  
        return tasks

    def query_exists(self, pk, user_id):
        exists = Task.objects.filter(id=pk, owner__id=user_id).exists()
        return exists



class User(AbstractUser):
    PERMISSION_CHOICES = [
        ('N','Normal'),
        ('A','Admin'),
    ]
    permission = models.CharField(max_length=1,
        choices=PERMISSION_CHOICES, default='N')
    
    @staticmethod
    def get_all_users(keyword):
        if keyword == None:
            keyword = ''
        users = User.objects.all().filter(username__icontains=keyword)
        return users

    @staticmethod
    def get_user_by_id(pk):
        user = User.objects.prefetch_related('task_set').get(pk=pk)
        return user

    def get_absolute_url(self):
        return reverse('main:uindex')
    


class Task(models.Model):
    objects = TaskManager()
    title = models.CharField(max_length=300)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    time_to_send = models.DateTimeField()
    precondition_tasks = models.ManyToManyField('Task', blank=True)

    class Meta:
       ordering = ['-time_to_send']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:index')
