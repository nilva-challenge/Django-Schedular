# Generated by Django 3.2.6 on 2021-08-05 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_task_precondition_task'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='precondition_task',
            new_name='precondition_tasks',
        ),
    ]