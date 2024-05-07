from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    SPACE_HOST = 'space_host'
    ADVERTISER = 'advertiser'

    ROLE_CHOICES = [
        (SPACE_HOST, 'Space Host'),
        (ADVERTISER, 'Advertiser')
    ]

    email = models.EmailField(unique=True)
    user_role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
