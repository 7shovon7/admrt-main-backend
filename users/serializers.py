from rest_framework import serializers
from .models import SpaceHost, Advertiser, AdvertiserProduct, Topic, SocialMedia, Portfolio, Language, PortfolioImageUploadFragment


# Profile Serializers
class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ['id', 'social_media', 'url']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertiserProduct
        fields = ['id', 'name', 'description', 'image']


class AdvertiserSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    socials = SocialMediaSerializer(many=True, read_only=True)
    joined = serializers.DateTimeField(source='user.date_joined', read_only=True)
    id = serializers.IntegerField(source='user.id', read_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    full_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = Advertiser
        fields = ['id', 'full_name', 'profile_image', 'banner_image', 'description', 'location', 'website', 'joined', 'products', 'socials', 'user']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title']


class PortfolioImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioImageUploadFragment
        fields = ['id', 'file']
        

class PortfolioSerializer(serializers.ModelSerializer):
    images = PortfolioImageUploadSerializer(many=True, read_only=True)
    class Meta:
        model = Portfolio
        fields = ['id', 'title', 'images', 'youtube_url']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'language']


class SpaceHostSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    portfolios = PortfolioSerializer(many=True, read_only=True)
    socials = SocialMediaSerializer(many=True, read_only=True)
    joined = serializers.DateTimeField(source='user.date_joined', read_only=True)
    id = serializers.IntegerField(source='user.id', read_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = SpaceHost
        fields = ['id', 'full_name', 'profile_image', 'banner_image', 'description', 'location', 'website', 'joined', 'long_term_service_availability', 'topics', 'languages', 'portfolios', 'socials', 'user']
