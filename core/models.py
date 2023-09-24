from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.core.validators import RegexValidator
from abc import ABC, abstractmethod


class Video(models.Model):
    file = models.FileField()
    url = models.URLField()


class UserManager(BaseUserManager, PermissionsMixin):
    def create_user(self, phone_number, password=None):
        """Creates and saves a User with number and password"""
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(phone_number)

        user.set_password(password)
        user.save(using=self.db)
        return user


class User(AbstractBaseUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    password_regex = RegexValidator(
        regex="^(?=.*?[0-9]).{8,}$",
        message="Password must be 8 to 16 characters and contain at least 1 digit."
    )

    phone_number = models.CharField(validators=[phone_regex],
                                    max_length=17,
                                    unique=True,
                                    )
    password = models.CharField(validators=[password_regex],
                                max_length=16,
                                )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone_number


class Statistics(ABC):
    date_created = models.DateTimeField(auto_now=True)

    @abc.abstractmethod
    def video(self):
        pass


class Watch(Statistics):
    def video(self):
        video = models.VideoField()
