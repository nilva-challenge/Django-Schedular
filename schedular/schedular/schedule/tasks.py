from .email import RealEmailService
from .services import SendEmailForTaskOwnerService
from celery import shared_task


@shared_task
def send_email_task(task_id: int):
    email_service = RealEmailService()
    send_email_service = SendEmailForTaskOwnerService(email_service=email_service)
    send_email_service.send_email_and_change_task_status(task_id=task_id)
    print(400 * '*')
    print(task_id)


@shared_task
def find_send_email_for_execute_task():
    from schedular.schedule.selectors import get_tasks_to_run
    get_tasks_to_run()
