from rest_framework import serializers
from .models import SpaceHost, Advertiser, AdvertiserProduct, Topic, SocialMedia, Portfolio, Language
        

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['id', 'social_media', 'username', 'url']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertiserProduct
        fields = ['id', 'name', 'description', 'image']


class AdvertiserSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    socials = SocialMediaSerializer(many=True)
    joined = serializers.DateTimeField(source='user.date_joined')
    id = serializers.IntegerField(source='user.id')
    full_name = serializers.CharField(source='user.full_name')
    email = serializers.EmailField(source='user.email')
    phone = serializers.CharField(source='user.phone')
    country = serializers.CharField(source='user.country')

    class Meta:
        model = Advertiser
        fields = ['id', 'full_name', 'profile_image', 'banner_image', 'description', 'location', 'country', 'email', 'phone', 'website', 'joined', 'products', 'socials']
        

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title']
        

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['id', 'title', 'file_url', 'youtube_url']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'language']


class SpaceHostSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True)
    languages = LanguageSerializer(many=True)
    portfolios = PortfolioSerializer(many=True)
    socials = SocialMediaSerializer(many=True)
    joined = serializers.DateTimeField(source='user.date_joined')
    id = serializers.IntegerField(source='user.id')
    full_name = serializers.CharField(source='user.full_name')
    email = serializers.EmailField(source='user.email')
    phone = serializers.CharField(source='user.phone')
    country = serializers.CharField(source='user.country')
    
    class Meta:
        model = SpaceHost
        fields = ['id', 'full_name', 'profile_image', 'banner_image', 'description', 'location', 'country', 'email', 'phone', 'website', 'joined', 'long_term_service_availability', 'topics', 'languages', 'portfolios', 'socials']
    