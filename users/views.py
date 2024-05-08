from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from core.serializers import UserSerializer
from .models import SpaceHost, Advertiser
from .serializers import SpaceHostSerializer, AdvertiserSerializer


class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = SpaceHostSerializer

    def list(self, request):
        try:
            user_role = request.user.user_role
            if user_role is None:
                user = settings.AUTH_USER_MODEL.objects.filter(user_id=request.user.id).first()
                serializer = UserSerializer
            if user_role == settings.K_SPACE_HOST_ID:
                user = SpaceHost.objects.filter(user=request.user.id).first()
                serializer = SpaceHostSerializer
            elif user_role == settings.K_ADVERTISER_ID:
                user = Advertiser.objects.filter(user=request.user.id).first()
                serializer = AdvertiserSerializer
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(serializer(user).data)
        except AttributeError:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'details': "No user found"})
