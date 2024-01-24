from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.db.models.signals import post_save, post_migrate
from django.contrib.auth import get_user_model
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def set_is_staff_ture_for_user_signal(sender, instance, created, **kwargs):
    if created:
        instance.is_staff = True
        instance.save()


@receiver(post_migrate)
def create_celery_periodic_task(sender, **kwargs):
    try:
        if not PeriodicTask.objects.filter(name='check_send_mail').exists():
            schedule, created = CrontabSchedule.objects.get_or_create(
                minute='*',
                hour='*',
                day_of_week='*',
                day_of_month='*',
                month_of_year='*',
            )

            periodic_task = PeriodicTask.objects.create(
                crontab=schedule,
                name='send_mail_task',
                task='schedular.schedule.tasks.find_send_email_for_execute_task',
                args='[]',
            )
    except Exception as e:
        print(f"error is {e}")
