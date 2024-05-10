from typing import Iterable
from django.conf import settings
from django.db import models


def change_filename(folder_path, original_filename, given_filename):
    file_parts = original_filename.split('.')
    if len(file_parts) > 1:
        updated_filename = f"{folder_path}/{given_filename}.{file_parts[-1]}"
    else:
        updated_filename = f"{folder_path}/{original_filename}"
    return updated_filename


def change_profile_image_filename(instance, filename):
    return change_filename(
        folder_path=f"profile/{instance.user.id}",
        original_filename=filename,
        given_filename='profile_image'
    )


def change_banner_image_filename(instance, filename):
    return change_filename(
        folder_path=f"profile/{instance.user.id}",
        original_filename=filename,
        given_filename='banner_image'
    )


def change_advertiser_product_image_filename(instance, filename):
    return change_filename(
        folder_path=f"profile/{instance.user.user.id}",
        original_filename=filename,
        given_filename='advertiser_product'
    )


def change_portfolio_image_filename(instance, filename):
    return change_filename(
        folder_path=f"profile/{instance.portfolio.user.user.id}/portfolios/{instance.portfolio.id}",
        original_filename=filename,
        given_filename='image'
    )


def change_product_image_filename(instance, filename):
    return change_filename(
        folder_path=f"profile/{instance.product.user.user.id}/products/{instance.product.id}",
        original_filename=filename,
        given_filename='image'
    )


class PlatformBaseUser(models.Model):
    profile_image = models.ImageField(upload_to=change_profile_image_filename, null=True, blank=True)
    banner_image = models.ImageField(upload_to=change_banner_image_filename, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name='profile')

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
    title = models.CharField(max_length=100)
    user = models.ForeignKey(SpaceHost, on_delete=models.CASCADE, related_name='topics')

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']


class AdvertiserProduct(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    # image = models.ImageField(upload_to=change_advertiser_product_image_filename, null=True, blank=True)
    user = models.ForeignKey(Advertiser, on_delete=models.CASCADE, related_name='products')

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['name']


class ProductImageUploadFragment(models.Model):
    file = models.ImageField(upload_to=change_product_image_filename)
    product = models.ForeignKey(AdvertiserProduct, related_name='images', on_delete=models.CASCADE)


class Language(models.Model):
    language = models.CharField(max_length=100)
    user = models.ForeignKey(SpaceHost, related_name='languages', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.language
    
    class Meta:
        ordering = ['language']


class Portfolio(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    # file_url = models.ImageField(upload_to=change_portfolio_image_filename, max_length=1024, null=True, blank=True)
    youtube_url = models.URLField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(SpaceHost, on_delete=models.CASCADE, related_name='portfolios')

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']


class PortfolioImageUploadFragment(models.Model):
    file = models.ImageField(upload_to=change_portfolio_image_filename)
    portfolio = models.ForeignKey(Portfolio, related_name='images', on_delete=models.CASCADE)


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
    # username = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(PlatformBaseUser, on_delete=models.CASCADE, related_name='socials')

    def __str__(self) -> str:
        if self.url is not None:
            return self.url
        elif self.username is not None:
            return self.username
        else:
            return None
