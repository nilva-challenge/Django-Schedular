from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_feedback_email_task(email_address):
    send_mail(
        "Your Feedback",
        f"\tdearali\n\nThank you!",
        'djangotest57@gmail.com',
        [email_address],
        fail_silently=False,
    )
