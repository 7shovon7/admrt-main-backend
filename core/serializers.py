from typing import Any, Dict
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenObtainPairSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'email', 'password', 'full_name', 'user_role']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'full_name', 'user_role']

class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.id
        # token['username'] = user.username
        token['email'] = user.email
        token['full_name'] = user.first_name
        # token['first_name'] = user.first_name
        # token['last_name'] = user.last_name
        token['user_role'] = user.user_role
        return token
    
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        data['user'] = {
            "id": self.user.id,
            # "username": self.user.username,
            "email": self.user.email,
            "full_name": self.user.full_name,
            # "first_name": self.user.first_name,
            # "last_name": self.user.last_name,
            "user_role": self.user.user_role
        }
        return data
