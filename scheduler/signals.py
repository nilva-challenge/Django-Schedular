from django.db.models.signals import pre_save
from django.dispatch import receiver
from scheduler.models import Task


@receiver(pre_save, sender=Task)
def set_owner(sender, instance, **kwargs):
    if not instance.owner and not instance.pk:
        instance.owner = request.user
