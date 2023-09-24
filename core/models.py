from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, UserManager, \
    PermissionsMixin
from django.core.validators import RegexValidator


class Video(models.Model):
    file = models.FileField()
    url = models.URLField()


class CustomUserManager(UserManager):
    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError("You must provide a phone")

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_stuff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_stuff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    password_regex = RegexValidator(
        regex="^(?=.*?[0-9]).{8,}$",
        message="Password must be 8 to 16 characters and contain at least 1 digit."
    )

    phone = models.CharField(validators=[phone_regex],
                             max_length=17,
                             unique=True,
                             )
    password = models.CharField(validators=[password_regex],
                                max_length=16,
                                )

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_stuff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = [phone, password]

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Statistics(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Watch(Statistics):
    video = models.FileField()
