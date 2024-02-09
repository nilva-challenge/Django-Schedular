from members.models import Member
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from scheduler.models import Task, TaskPermission


@receiver(post_save, sender=Member)
def assign_permissions(sender, instance, created, **kwargs):
    if not instance.is_superuser and created:
        instance.is_staff = True

        content_type = ContentType.objects.get_for_model(Task)

        view_permission = Permission.objects.get(
            codename=TaskPermission.ADD_TASK.value,
            content_type=content_type,
        )
        view_permission = Permission.objects.get(
            codename=TaskPermission.VIEW_TASK.value,
            content_type=content_type,
        )
        change_permission = Permission.objects.get(
            codename=TaskPermission.CHANGE_TASK.value,
            content_type=content_type,
        )
        delete_permission = Permission.objects.get(
            codename=TaskPermission.DELETE_TASK.value,
            content_type=content_type,
        )

        instance.user_permissions.add(
            view_permission, change_permission, delete_permission
        )

        instance.save()
