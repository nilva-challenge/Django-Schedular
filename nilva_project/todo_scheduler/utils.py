from nilva_project.celeryapp import celery_app
from .tasks import send_reminder_email


def remove_current_task(id):
    celery_app.control.revoke(id)


def set_new_task(countdown,email):
    if countdown < 0:
        return None
    else:
        return send_reminder_email.apply_async((email,),countdown=countdown)