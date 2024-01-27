from django.core.mail import send_mail
from celery import shared_task



@shared_task()
def send_status_of_task_email_task(email_address, message):
    """Sends an email when the feedback form has been submitted."""
    send_mail(
        "Your Task",
        f"\t{message}\n\nThank you!",
        "support@example.com",
        [email_address],
        fail_silently=False,
    )