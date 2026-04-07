from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    birth_date = models.DateField(blank=True, null=True)
    first_name = models.CharField(blank=True, null=True)
    last_name = models.CharField(blank=True, null=True)

    class AuthSource(models.TextChoices):
        LOCAL = 'local', 'Local'
        GOOGLE = 'google', 'Google'
        GITHUB = 'github', 'GitHub'

    auth_source = models.CharField(
        max_length=20,
        choices=AuthSource.choices,
        default=AuthSource.LOCAL
    )
    objects = CustomUserManager()

    REQUIRED_FIELDS = ['phone_number',]
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

