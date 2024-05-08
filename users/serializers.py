from rest_framework import serializers
from .models import SpaceHost, Advertiser


class AdvertiserSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    socials = serializers.SerializerMethodField()

    class Meta:
        model = Advertiser
        fields = ['profile_image', 'banner_image', 'description', 'location', 'website', 'joined', 'products', 'socials']
    
    def get_products(self, obj):
        try:
            return [{"name": p.name, "description": p.description, "image": p.image} for p in obj.products.all()]
        except AttributeError:
            return []
    
    def get_socials(self, obj):
        try:
            return [{"social_media": s.social_media, "username": s.username, "url": s.url} for s in obj.socials.all()]
        except AttributeError:
            return []


class SpaceHostSerializer(serializers.ModelSerializer):
    topics = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    portfolios = serializers.SerializerMethodField()
    socials = serializers.SerializerMethodField()
    
    class Meta:
        model = SpaceHost
        fields = ['profile_image', 'banner_image', 'description', 'location', 'website', 'joined', 'long_term_service_availability', 'topics', 'languages', 'portfolios', 'socials']
    
    def get_topics(self, obj):
        try:
            return [topic.title for topic in obj.topics.all()]
        except AttributeError:
            return []
    
    def get_languages(self, obj):
        try:
            return [language.language for language in obj.languages.all()]
        except AttributeError:
            return []
    
    def get_portfolios(self, obj):
        try:
            return [{"title": p.title, "file_url": p.file_url, "youtube_url": p.youtube_url} for p in obj.portfolios.all()]
        except AttributeError:
            return []
    
    def get_socials(self, obj):
        try:
            return [{"social_media": s.social_media, "username": s.username, "url": s.url} for s in obj.socials.all()]
        except AttributeError:
            return []
