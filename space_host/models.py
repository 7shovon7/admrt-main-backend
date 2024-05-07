from typing import Iterable
from django.conf import settings
from django.db import models


class SpaceHost(models.Model):
    profile_image = models.URLField(max_length=1024, null=True, blank=True)
    banner_image = models.URLField(max_length=1024, null=True, blank=True)
    topics = models.ManyToManyField('Topic', related_name='users')
    intro = models.TextField(null=True, blank=True)
    long_term_service_availability = models.CharField(max_length=100, null=True, blank=True)
    languages = models.ManyToManyField('Language', related_name='users')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.full_name
    
    class Meta:
        ordering = ['user__full_name']


class Topic(models.Model):
    # name = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']


class Language(models.Model):
    language = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.language
    
    class Meta:
        ordering = ['language']


class Portfolio(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    file_url = models.URLField(max_length=1024, null=True, blank=True)
    youtube_url = models.URLField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(SpaceHost, on_delete=models.CASCADE, related_name='portfolios')

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']
