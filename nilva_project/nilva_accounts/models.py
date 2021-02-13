from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


def access_users_to_admin_panel(sender,instance,*args,**kwargs):
    if not instance.is_staff:
        instance.is_staff = True

pre_save.connect(access_users_to_admin_panel , User)
