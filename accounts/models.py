from typing import Optional
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    biography = models.TextField(blank=True, null=True)

    phone_number = models.CharField(max_length=11, blank=True, null=True)
    email = models.EmailField(
        max_length=255, unique=True, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f'{self.username}'

    @property
    def is_staff(self):
        return self.is_admin
