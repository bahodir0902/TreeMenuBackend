from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    objects = CustomUserManager()

    class Meta:
        db_table = "Users"
        verbose_name = "User"
        verbose_name_plural = "Users"
