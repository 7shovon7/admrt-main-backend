from django.conf import settings
from django.db import models


class SpaceHost(models.Model):
    profile_image = models.URLField(max_length=1024, null=True, blank=True)
    banner_image = models.URLField(max_length=1024, null=True, blank=True)
    expertise = models.ManyToManyField('Expertise', null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class Expertise(models.Model):
    topic = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return str(self.topic)
    
    class Meta:
        ordering = ['topic']
        