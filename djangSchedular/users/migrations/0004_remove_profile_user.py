# Generated by Django 3.2.9 on 2021-11-26 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_permissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
    ]
