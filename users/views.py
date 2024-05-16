from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.serializers import UserSerializer
from .models import SpaceHost, Advertiser, Topic, Language, Portfolio, SocialMedia, AdvertiserProduct
from .serializers import SpaceHostSerializer, AdvertiserSerializer, TopicSerializer, LanguageSerializer, PortfolioSerializer, SocialMediaSerializer, ProductSerializer
from .utils import object_is_not_related


class AdvertiserProductViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return AdvertiserProduct.objects.filter(user=self.request.user.id).all()
    
    def create(self, request, *args, **kwargs):
        related_object_issue = object_is_not_related(request.user.profile, 'advertiser')
        if related_object_issue:
            return related_object_issue
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
        else:
            serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user.profile.advertiser)
    

class SocialMediaViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SocialMediaSerializer

    def get_queryset(self):
        return SocialMedia.objects.filter(user=self.request.user.id).all()
    
    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
        else:
            serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user.profile)


class PortfolioViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PortfolioSerializer

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user.id).all()
    
    def create(self, request, *args, **kwargs):
        related_object_issue = object_is_not_related(request.user.profile, 'spacehost')
        if related_object_issue:
            return related_object_issue
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
        else:
            serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user.profile.spacehost)


class LanguageViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LanguageSerializer

    def get_queryset(self):
        return Language.objects.filter(user=self.request.user.id).all()
    
    def create(self, request, *args, **kwargs):
        related_object_issue = object_is_not_related(request.user.profile, 'spacehost')
        if related_object_issue:
            return related_object_issue
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
        else:
            serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user.profile.spacehost)


class TopicViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TopicSerializer

    def get_queryset(self):
        return Topic.objects.filter(user=self.request.user.id).all()
    
    def create(self, request, *args, **kwargs):
        related_object_issue = object_is_not_related(request.user.profile, 'spacehost')
        if related_object_issue:
            return related_object_issue
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
        else:
            serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user.profile.spacehost)


class UserViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        requested_user_id = self.request.GET.get('id')
        if requested_user_id is not None:
            user_id = requested_user_id
        else:
            user_id = self.request.user.id
        # Fetch the user profile
        queryset = get_user_model().objects.filter(id=user_id).first().profile
        if hasattr(queryset, 'spacehost'):
            self.serializer_class = SpaceHostSerializer
            queryset = queryset.spacehost
        elif hasattr(queryset, 'advertiser'):
            self.serializer_class = AdvertiserSerializer
            queryset = queryset.advertiser
        else:
            queryset = None
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        # serializer_class = self.get_serializer_class()
        serializer = self.serializer_class(queryset, many=False)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"details": "Profile creation should have been done at the registration level. Seems like that was not done. Something went wrong."})
        else:
            serializer = self.get_serializer(queryset, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        
