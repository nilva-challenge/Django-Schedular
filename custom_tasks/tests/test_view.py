from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Task
import pytest
from ..serializers import TaskSerializer
from .factory import create_fake_task, create_fake_user

import django
django.setup()


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_task_list():
    # Create a test user
    user = create_fake_user()

    # Create some test tasks
    task_1 = create_fake_task(owner=user, has_precondition_tasks=False)


    # Set up the API client
    client = APIClient()
    client.force_authenticate(user=user)

    # Test retrieving tasks
    url = reverse('task-validation') 
    response = client.get(url)
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data
    
    
@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_only_owner_permission():
    # Create a test user
    user1 = create_fake_user()
    user2 = create_fake_user() 

    # Create some test tasks
    task_1 = create_fake_task(owner=user1, has_precondition_tasks=False)
    task_2 = create_fake_task(owner=user2, has_precondition_tasks=False)
    

    # Set up the API client
    client = APIClient()
    client.force_authenticate(user=user1)

    # Test retrieving tasks
    url = reverse('task-validation') 
    response = client.get(url)
    tasks = Task.objects.filter(owner=user1)
    serializer = TaskSerializer(tasks, many=True)
    print(response.data)
    print(serializer.data) 
    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data
    
    