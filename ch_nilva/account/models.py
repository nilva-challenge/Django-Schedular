from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_staff = models.BooleanField(default=True, verbose_name='staff status')
    is_admin = models.BooleanField(default=False, verbose_name='admin status')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'
