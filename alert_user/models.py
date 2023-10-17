from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager, make_password
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError

from alert_user.validators import iran_mobile_phone_number_validator

from email_normalize import normalize as normalize_email


class AlertUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given password.
        """
        normalized_email = normalize_email(email).normalized_address
        user = self.model(email=normalized_email, password=make_password(password), **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("email_alert", True)
        return self.create_user(email, password, **extra_fields)


class AlertUser(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(default=False, help_text="Designates whether the user can log into admin site.")
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        unique=True,
        help_text="Adjusted for Iran's phone number format."
        "Modify this field If you want to use this project in a different country",
        validators=[iran_mobile_phone_number_validator],
    )
    telegram_id = models.BigIntegerField(blank=True, null=True, unique=True)
    sms_alert = models.BooleanField(default=False)
    email_alert = models.BooleanField(default=False)
    telegram_message_alert = models.BooleanField(default=False)

    objects = AlertUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
        if not self.sms_alert and not self.email_alert and not self.telegram_message_alert:
            raise ValidationError("There must be at least one way to alert user", code="one_way_to_alert")

        if self.phone == "":
            self.phone = None
        if self.telegram_id == "":
            self.telegram_id = None

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
