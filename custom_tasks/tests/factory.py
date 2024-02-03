from faker import Faker
from django.contrib.auth import get_user_model
from ..models import Task

fake = Faker()

def create_fake_user(username=None, password=None, email=None, permissions='normal'):
    username = username or fake.unique.user_name()
    password = password or fake.password()
    email = email or fake.unique.email()
    return get_user_model().objects.create_user(username=username, password=password, permissions=permissions, email=email)

def create_fake_task(owner, title=None, description=None, time_to_send=None, precondition_tasks=None, has_precondition_tasks=False):
    title = title or fake.word()
    description = description or fake.sentence()
    time_to_send = time_to_send or fake.date_time_this_decade()
    if has_precondition_tasks:
        task =  Task.objects.create(owner=owner, title=title, description=description, time_to_send=time_to_send)
        precondition_tasks = precondition_tasks or create_fake_task(owner=owner)
        task.precondition_tasks.add(precondition_tasks)
        task.save()
    else:
        precondition_tasks = None
        task =  Task.objects.create(owner=owner, title=title, description=description, time_to_send=time_to_send)
    
    return task