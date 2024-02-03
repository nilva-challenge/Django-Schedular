# test_task_validator.py
from ..models import TaskValidator
import pytest
from .factory import create_fake_task, create_fake_user
from datetime import timedelta
from django.utils import timezone
from celery import Celery
from django.conf import settings
from celery.contrib.testing.worker import start_worker
from celery.contrib.testing import tasks as test_tasks

app = Celery('TaskScheduler')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Use Celery's testing mixin for pytest
@pytest.fixture
def celery_worker(request):
    with start_worker(app, perform_ping_check=False) as w:
        yield w


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_task_validator_valid():
    current_datetime = timezone.now()
    # Define a timedelta representing a duration of 30 minutes
    time_difference = timedelta(minutes=30)
    # Subtract the timedelta from the current datetime to get another datetime
    previous_datetime = current_datetime - time_difference
    
    user = create_fake_user()
    task1 = create_fake_task(owner=user, time_to_send=previous_datetime, has_precondition_tasks=False)
    task2 = create_fake_task(owner=user, time_to_send=current_datetime, precondition_tasks=task1, has_precondition_tasks=True)
    validator1 = TaskValidator(task1)
    validator2 = TaskValidator(task2)
    
    assert validator1.is_valid() == True
    assert validator2.is_valid() == True


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_task_validator_valid():
    current_datetime = timezone.now()
    # Define a timedelta representing a duration of 30 minutes
    time_difference = timedelta(minutes=30)
    # Subtract the timedelta from the current datetime to get another datetime
    next_datetime = current_datetime + time_difference
    
    user = create_fake_user()
    task1 = create_fake_task(owner=user, time_to_send=next_datetime, has_precondition_tasks=False)
    task2 = create_fake_task(owner=user, time_to_send=current_datetime, precondition_tasks=task1, has_precondition_tasks=True)
    print(task2.precondition_tasks)
    validator1 = TaskValidator(task1)
    validator2 = TaskValidator(task2)
    
    assert validator1.is_valid() == True
    assert validator2.is_valid() == False


