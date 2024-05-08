from django.conf import settings
from rest_framework import permissions
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.serializers import UserSerializer
from .models import SpaceHost, Advertiser
from .serializers import SpaceHostSerializer, AdvertiserSerializer


class UserViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, GenericViewSet):
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
