from typing import Any, Dict
from django.conf import settings
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenObtainPairSerializer

from users.models import SpaceHost, Advertiser


class UserCreateSerializer(BaseUserCreateSerializer):
    username = serializers.CharField(read_only=True)
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'password', 'full_name', 'phone', 'country', 'user_role']

    def create(self, validated_data):
        user = super().create(validated_data)
        user_role = validated_data.get('user_role')
        
        profile_class = None
        if user_role == settings.K_SPACE_HOST_ID:
            profile_class = SpaceHost
        elif user_role == settings.K_ADVERTISER_ID:
            profile_class = Advertiser
        if profile_class is not None:
            profile_class.objects.create(user=user)
        
        return user


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'full_name', 'phone', 'country', 'user_role']

class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        if hasattr(user, 'profile'):
            image_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{user.profile.profile_image}"
        token['id'] = user.id
        token['email'] = user.email
        token['username'] = user.username
        token['full_name'] = user.full_name
        token['profile_image'] = image_url
        # token['phone'] = user.phone
        # token['country'] = user.country
        token['user_role'] = user.user_role
        return token
    
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        if hasattr(self.user, 'profile'):
            image_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{self.user.profile.profile_image}"
        else:
            image_url = None
        data['user'] = {
            "id": self.user.id,
            "email": self.user.email,
            "username": self.user.username,
            "full_name": self.user.full_name,
            "profile_image": image_url,
            "phone": self.user.phone,
            "country": self.user.country,
            "user_role": self.user.user_role
        }
        return data
