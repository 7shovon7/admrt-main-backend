from django.conf import settings
from django.db.models import Q
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
        # Search terms
        search_terms = self.request.GET.get('q').split(' ')
        if len(search_terms) > 0 and user_role == settings.K_ADVERTISER_ID:
            # Build the query
            query = Q()
            # Conditions for PlatformBaseUser
            for term in search_terms:
                query |= Q(user__full_name__icontains=term)
            # Conditions for SpaceHost
            for term in search_terms:
                query |= Q(location__icontains=term) | \
                        Q(description__icontains=term)
            queryset = SpaceHost.objects.all().filter(query)
        else:
            queryset = None
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        # serializer_class = self.get_serializer_class()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
