from django.db import models
from schedular.common.models import BaseModel
from django.contrib.auth.models import AbstractUser


class BaseUser(BaseModel, AbstractUser):
    pass





