from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

from scheduler.models import Task, TaskPermission
from django.contrib.auth.models import ContentType, Permission


def create_task_permissions(apps, schema_editor):
    content_type = ContentType.objects.get_for_model(Task)

    Permission.objects.get_or_create(
        codename=TaskPermission.ADD_TASK,
        name="Can add tasks",
        content_type=content_type,
    )

    Permission.objects.get_or_create(
        codename=TaskPermission.VIEW_TASK,
        name="Can view tasks",
        content_type=content_type,
    )

    Permission.objects.get_or_create(
        codename=TaskPermission.CHANGE_TASK,
        name="Can update tasks",
        content_type=content_type,
    )

    Permission.objects.get_or_create(
        codename=TaskPermission.DELETE_TASK,
        name="Can delete tasks",
        content_type=content_type,
    )


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(create_task_permissions),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("time_to_send", models.DateTimeField()),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "precondition_tasks",
                    models.ManyToManyField(blank=True, to="scheduler.task"),
                ),
            ],
        ),
    ]
