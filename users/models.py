from django.contrib.auth.models import AbstractUser, Permission
from django.db import models


class Member(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=False, unique=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    def set_permissions(self):
        if self.is_staff:
            permission_handles = ['Can add user', 'Can change user', 'Can delete user', 'Can view user']
            for p in permission_handles:
                permission = Permission.objects.get(name=p)
                self.user_permissions.add(permission)
