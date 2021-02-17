from celery import shared_task
from celery.utils.log import get_task_logger

from django.core.mail import send_mail

from Scheduler.settings import EMAIL_HOST_USER

logger = get_task_logger(__name__)


@shared_task(name="send_scheduled_mail")
def send_scheduled_mail(email):

    logger.info("Sent scheduled email")
    message = "This message was scheduled to be sent to you automatically by " \
              "the django scheduler"
    return send_mail('reminder', message, EMAIL_HOST_USER, [email], fail_silently=False)
