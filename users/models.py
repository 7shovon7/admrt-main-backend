from django.conf import settings
from django.db import models


class PlatformBaseUser(models.Model):
    profile_image = models.URLField(max_length=1024, null=True, blank=True)
    banner_image = models.URLField(max_length=1024, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.full_name


class SpaceHost(PlatformBaseUser):
    long_term_service_availability = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.full_name

    def save(self, *args, **kwargs):
        if not self.user.user_role == settings.K_SPACE_HOST_ID:
            print(f"user needs to have role of {settings.K_SPACE_HOST_ID} to be saved in SpaceHost model")
        else:
            return super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['user__full_name']


class Advertiser(PlatformBaseUser):
    def __str__(self) -> str:
        return self.user.full_name

    def save(self, *args, **kwargs):
        if not self.user.user_role == settings.K_ADVERTISER_ID:
            print(f"user needs to have role of {settings.K_ADVERTISER_ID} to be saved in Advertiser model")
        else:
            return super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['user__full_name']


class Topic(models.Model):
    title = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(SpaceHost, on_delete=models.CASCADE, related_name='topics')

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']


class AdvertiserProduct(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.URLField(max_length=1024, null=True, blank=True)
    user = models.ForeignKey(Advertiser, on_delete=models.CASCADE, related_name='products')

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['name']


class Language(models.Model):
    language = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(SpaceHost, related_name='languages', on_delete=models.CASCADE)

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


class SocialMedia(models.Model):
    FACEBOOK = 'fb'
    YOUTUBE = 'yt'
    LINKEDIN = 'ln'
    INSTAGRAM = 'in'
    X = 'x'
    TIKTOK = 'tt'
    WHATSAPP = 'wa'

    SM_CHOICES = [
        (FACEBOOK, 'Facebook'),
        (YOUTUBE, 'YouTube'),
        (LINKEDIN, 'LinkedIn'),
        (INSTAGRAM, 'Instagram'),
        (X, 'X'),
        (TIKTOK, 'TikTok'),
        (WHATSAPP, 'WhatsApp'),
    ]

    social_media = models.CharField(max_length=2, choices=SM_CHOICES)
    username = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(PlatformBaseUser, on_delete=models.CASCADE, related_name='socials')

    def __str__(self) -> str:
        if self.url is not None:
            return self.url
        elif self.username is not None:
            return self.username
        else:
            return None
