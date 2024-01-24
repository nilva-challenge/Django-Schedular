from django.contrib.auth.models import AbstractUser
from schedular.common.models import BaseModel
from django.db import models


class BaseUser(BaseModel, AbstractUser):
    pass





