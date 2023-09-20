from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from model_utils.models import TimeStampedModel

from .managers import UserManager


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):  # todo Put the Timestamp

    GENDER_CHOICES = (
        ('M', 'Men'),
        ('F', 'Female'),
        ('O', 'Others'),
    )

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(default=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    # PermisionMixin requerided fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    objects = UserManager()
