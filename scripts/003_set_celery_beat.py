from django_celery_beat.models import CrontabSchedule, PeriodicTask

scheduler_every_minute = CrontabSchedule.objects.filter(
    minute="*",
    hour="*",
    day_of_week="*",
    day_of_month="*",
).first()

if not scheduler_every_minute:
    scheduler_every_minute = CrontabSchedule.objects.create(
        minute="*",
        hour="*",
        day_of_week="*",
        day_of_month="*",
    )

PeriodicTask.objects.get_or_create(
    name="send email every minute", task="task.tasks.send_tasks_email", crontab_id=scheduler_every_minute.id
)
