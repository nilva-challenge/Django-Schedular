from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid
from pydantic import EmailStr


class CustomUserManager(BaseUserManager):
    def create_user(self, username: str, email: EmailStr, password: str = None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(username) if password is None else user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username: str, email: EmailStr, password: str = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    objects = CustomUserManager()

    def __str__(self):
        return str(self.id)


class Task(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=128)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    time_to_send = models.DateTimeField()
    precondition_tasks = models.ManyToManyField('self', blank=True)
    is_done = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def are_precondition_tasks_done(self):
        return self.precondition_tasks.filter(is_done=True).count() == self.precondition_tasks.count()

    def __str__(self):
        return (
            f"title: {self.title}, task_id: {str(self.id)},"
            f" owner_id: {self.owner}, owner_full_name: {self.owner.get_full_name()}"
        )
