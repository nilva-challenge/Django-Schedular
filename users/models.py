from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    permissions = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('normal', 'Normal')])

    # Add any additional fields you need for users

    def __str__(self):
        return self.username
    

@receiver(post_save, sender=CustomUser)
def make_user_staff(sender, instance, created, **kwargs):
    if created:
        instance.is_staff = True
        instance.save()