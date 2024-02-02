from django.shortcuts import render, HttpResponse
from .tasks import send_task_email
from .models import Task

# Create your views here.
def create_task(request):
    # Your view logic to create a task
    # task = Task.objects.create(...)  # Replace with actual task creation logic
    task = Task.objects.first()
    # Schedule the send_task_email task asynchronously
    send_task_email.apply_async(args=[task.id], eta=task.time_to_send)

    response_text = "Hello, this is a simple text response."
    
    # Create an HttpResponse with the text content
    response = HttpResponse(response_text, content_type='text/plain')

    return response