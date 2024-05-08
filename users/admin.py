from django.contrib import admin
from .models import SpaceHost, Topic, Language, Portfolio, SocialMedia, Advertiser, AdvertiserProduct


admin.site.register([SpaceHost, Topic, Language, Portfolio, SocialMedia, Advertiser, AdvertiserProduct])