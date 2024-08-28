from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone
from django.utils.crypto import get_random_string

from core.utils import generate_username_from_email


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        username = generate_username_from_email(email)
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)
    
    
class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        if isinstance(value, str):
            return value.lower()
        return value


class User(AbstractUser):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("email"),
                name="user_email_ci_uniqueness",
            ),
        ]
    ROLE_CHOICES = [
        (settings.K_SPACE_HOST_ID, 'Space Host'),
        (settings.K_ADVERTISER_ID, 'Advertiser')
    ]

    email = LowercaseEmailField(unique=True)
    phone = models.CharField(max_length=20)
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=60)
    birthday = models.DateField(null=True, blank=True)
    user_role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    
    reset_code = models.CharField(max_length=6, null=True, blank=True)
    reset_code_expiry = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'full_name', 'country']

    objects = UserManager()
    
    def set_reset_code(self):
        self.reset_code = self._generate_reset_code()
        self.reset_code_expiry = timezone.now() + timedelta(minutes=10)
        self.save()

    def _generate_reset_code(self):
        return get_random_string(6, allowed_chars='0123456789')

    def validate_reset_code(self, code):
        if self.reset_code == code and self.reset_code_expiry and timezone.now() < self.reset_code_expiry:
            return True
        return False

    def clear_reset_code(self):
        self.reset_code = None
        self.reset_code_expiry = None
        self.save()
