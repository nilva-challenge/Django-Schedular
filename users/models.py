from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'  # Set email as the login identifier
    REQUIRED_FIELDS = ['username']  # Keep username, but it's no longer required for authentication

    def __str__(self):
        return self.email  # Or keep it as self.username, depending on your preference

    def save(self, *args, **kwargs):
        self.email = self.email.lower()  # Optional: Ensuring email is always stored in lowercase
        super().save(*args, **kwargs)
