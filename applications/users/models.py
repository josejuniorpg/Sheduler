# Django imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Packages imports
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

# Local imports
from .managers import UserManager


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    GENDER_CHOICES = (
        ('1', 'Men'),
        ('2', 'Female'),
        ('3', 'Others'),
    )

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(default=True)  # todo maybe change the name to is_delete
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    code_verification = models.CharField(max_length=6, blank=True)  # Todo Configure  code verification email.
    phone_number = PhoneNumberField(blank=True) #todo make unique phone
    profile_image = models.ImageField(upload_to='users/profileImages', blank=True, null=True)

    # PermissionMixin required fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'is_staff', 'is_active', 'is_superuser', 'first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        template = f'{self.first_name}, {self.last_name}, {self.email}, {self.username}, ID: {self.id}'
        return template.format(self)

    def get_short_name(self):
        return self.first_name
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
    def get_username(self):
        return self.username
