from celery import Celery
from .views import send_emails

app = Celery()
@app.task
def trigger_emails():
    send_emails()
