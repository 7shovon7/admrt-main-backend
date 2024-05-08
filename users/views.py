from django.conf import settings
from rest_framework import permissions, status, generics
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.serializers import UserSerializer
from .models import SpaceHost, Advertiser, Topic
from .serializers import SpaceHostSerializer, AdvertiserSerializer, TopicSerializer


class TopicListCreateAPIView(ListModelMixin, CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TopicSerializer

    def get_queryset(self):
        return Topic.objects.filter(user=self.request.user.id).all()
    
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
        return serializer.save(user=self.request.user.profile.spacehost)


class UserViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user_role = self.request.user.user_role
        user_id = self.request.user.id
        if user_role is not None:
            if user_role == settings.K_SPACE_HOST_ID:
                queryset = SpaceHost.objects.filter(user=user_id).first()
            elif user_role == settings.K_ADVERTISER_ID:
                queryset = Advertiser.objects.filter(user=user_id).first()
            else:
                queryset = settings.AUTH_USER_MODEL.objects.filter(user_id=user_id).first()
        else:
            queryset = None
        return queryset

    def get_serializer_class(self):
        serializer_class = UserSerializer
        user_role = self.request.user.user_role
        if user_role is not None:
            if user_role == settings.K_SPACE_HOST_ID:
                serializer_class = SpaceHostSerializer
            elif user_role == settings.K_ADVERTISER_ID:
                serializer_class = AdvertiserSerializer
        return serializer_class

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=False)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return super().create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(queryset, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
