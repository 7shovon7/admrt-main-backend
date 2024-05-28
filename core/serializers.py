from typing import Any, Dict
from django.conf import settings
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenObtainPairSerializer

from core.models import User
from core.utils import get_profile_image_url
from users.models import SpaceHost, Advertiser


class UserCreateSerializer(BaseUserCreateSerializer):
    username = serializers.CharField(read_only=True)
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'password', 'full_name', 'phone', 'country', 'birthday', 'user_role']

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
        fields = ['id', 'username', 'email', 'full_name', 'phone', 'country', 'birthday', 'user_role']
        
        
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'country', 'birthday', 'user_role']
        read_only_fields = ['email', 'user_role']
        
        
class UserPartialUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'phone', 'country', 'birthday']
        

class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        image_url = None
        is_admin = None
        if hasattr(user, 'profile'):
            image_url = get_profile_image_url(user.profile.profile_image)
            is_admin = user.profile.is_admin
        token['id'] = user.id
        token['email'] = user.email
        token['username'] = user.username
        token['full_name'] = user.full_name
        token['profile_image'] = image_url
        token['is_admin'] = is_admin
        token['user_role'] = user.user_role
        return token
    
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        image_url = None
        is_admin = None
        if hasattr(self.user, 'profile'):
            image_url = get_profile_image_url(self.user.profile.profile_image)
            is_admin = self.user.profile.is_admin
        data['user'] = {
            "id": self.user.id,
            "email": self.user.email,
            "username": self.user.username,
            "full_name": self.user.full_name,
            "profile_image": image_url,
            "is_admin": is_admin,
            "phone": self.user.phone,
            "country": self.user.country,
            "user_role": self.user.user_role
        }
        return data
