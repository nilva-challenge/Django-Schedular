# Generated by Django 5.0.1 on 2024-01-21 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_remove_task_pre_tasks_pretask_task_pre_tasks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='pre_tasks',
        ),
        migrations.AddField(
            model_name='task',
            name='pre_tasks',
            field=models.ManyToManyField(blank=True, null=True, to='task.pretask'),
        ),
    ]
