# Generated by Django 5.0.2 on 2024-03-01 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='sent_at',
            field=models.DateTimeField(default=None),
        ),
    ]