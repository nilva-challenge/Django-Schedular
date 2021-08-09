from django.test import TestCase
from .models import Task, User
from datetime import datetime, timezone
from django.urls import reverse
from .forms import TaskCreateForm

class TaskTest(TestCase):

    def create_task(self, title, description, owner, time_to_send):
        
        return Task.objects.create(
            title=title,
            description=description,
            owner=owner,
            time_to_send=time_to_send
        )


    def test_creation_task(self):
        user = User.objects.get(id=1)
        task = self.create_task(
            'test',
            'testtt',
            user,
            datetime.now(timezone.utc)
        )
        self.assertTrue(isinstance(task, Task))
    

    def test_task_list_view(self):
        url = reverse("main:index")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)


    def test_task_create_view(self):
        url = reverse("main:create")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)


    def test_valid_form(self):
        user = User.objects.get(id=1)
        task = self.create_task(
            'test',
            'testtt',
            user,
            datetime.now(timezone.utc)
        )
        data = {
            'title': task.title, 
            'description': task.description,
            'time_to_send': task.time_to_send,
            'owner_id':1
        }
        form = TaskCreateForm(data=data)
        self.assertTrue(form.is_valid())
