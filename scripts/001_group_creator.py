from time import sleep

from django.contrib.auth.models import Group, Permission


def group_creators():
    # if it has data do not any work
    groups = Group.objects.first()
    if groups:
        return

    sleep(10)

    # user permissions
    user_permissions = Permission.objects.filter(codename__in=["add_user", "change_user", "delete_user", "view_user"])

    # task permissions
    task_permissions = Permission.objects.filter(codename__in=["add_task", "change_task", "delete_task", "view_task"])

    # add admin group in database
    admin_group = Group.objects.create(
        name="Admin",
    )
    admin_group.permissions.add(*user_permissions, *task_permissions)

    # add user group in database
    user_group = Group.objects.create(
        name="User",
    )
    user_group.permissions.add(*task_permissions)


group_creators()
