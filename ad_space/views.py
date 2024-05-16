from django.conf import settings
from rest_framework import permissions
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.models import SpaceHost
from users.serializers import SpaceHostSerializer


class AdSpaceViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SpaceHostSerializer
    # queryset = SpaceHost.objects.all()
    
    def get_queryset(self):
        user_role = self.request.user.user_role
        user_id = self.request.user.id
        print(self.request.user.id)
        if user_role == settings.K_ADVERTISER_ID:
            queryset = SpaceHost.objects.all().filter(description__contains="fans, max brings")
        else:
            queryset = None
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        # serializer_class = self.get_serializer_class()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
