from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.core.mail import send_mail
from django.shortcuts import render

def send_test_email(request):
    send_mail(
        'Subject',
        'Message body',
        'zarrinmorteza137958@gmail.com', # Sender's email address
        ['m.zarrin95@gmail.com'],  # Recipient's email address
        fail_silently=False,
    )
    response_text = "Hello, this is a simple text response."
    
    # Create an HttpResponse with the text content
    response = HttpResponse(response_text, content_type='text/plain')

    return response