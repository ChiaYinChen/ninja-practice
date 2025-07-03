from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from .managers import CustomUserManager


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False, db_default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = "USER"
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email
