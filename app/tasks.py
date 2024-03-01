from django.core.mail import send_mail
from celery import shared_task
from django.utils import timezone
from .models import Task
from celery import current_app

@shared_task
def send_email(title, description, owner_email, task_id):
    """
    Sends an email and updates the 'sent_at' field of the associated Task.

    Args:
        title (str): The title of the task, used as the email subject.
        description (str): The description of the task, used as the email message.
        owner_email (str): The email address of the task owner.
        task_id (int): The ID of the associated Task in the database.

    Returns:
        None

    Raises:
        Task.DoesNotExist: If the Task with the specified task_id does not exist.

    Note:
        This function uses the Django send_mail function to send an email to the task owner.
        It updates the 'sent_at' field of the associated Task to mark it as sent.
    """
    task = Task.objects.get(id=task_id)

    subject = title
    message = description
    from_email = 'djangotest57@gmail.com'
    recipient_list = [owner_email]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )

    task.sent_at = timezone.now()
    task.save()
