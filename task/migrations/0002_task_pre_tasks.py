# Generated by Django 5.0.1 on 2024-01-21 12:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='pre_tasks',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='task.task'),
            preserve_default=False,
        ),
    ]
