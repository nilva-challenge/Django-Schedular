# Generated by Django 3.2.6 on 2021-08-05 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='permission',
            field=models.CharField(choices=[('N', 'Normal'), ('A', 'Admin')], default='N', max_length=1),
        ),
    ]
