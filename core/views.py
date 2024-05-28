from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)

from .models import User
from .serializers import UserDetailSerializer, UserPartialUpdateSerializer

class UserViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def settings(self, request):
    #     user = self.request.user
    #     serializer = self.get_serializer(user)
    #     return Response(serializer.data)

    def list(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserPartialUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # def update_settings(self, request):
    #     user = self.request.user
    #     serializer = UserPartialUpdateSerializer(user, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=400)
    
    
# class UserViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = UserDetailSerializer

#     def get_queryset(self):
#         requested_user_id = self.request.GET.get('id')
#         if requested_user_id is not None:
#             user_id = requested_user_id
#         else:
#             user_id = self.request.user.id
#         # Fetch the user profile
#         queryset = get_user_model().objects.filter(id=user_id).first().profile
#         if hasattr(queryset, 'spacehost'):
#             self.serializer_class = SpaceHostSerializer
#             queryset = queryset.spacehost
#         elif hasattr(queryset, 'advertiser'):
#             self.serializer_class = AdvertiserSerializer
#             queryset = queryset.advertiser
#         else:
#             queryset = None
#         return queryset

#     def list(self, request):
#         queryset = self.get_queryset()
#         # serializer_class = self.get_serializer_class()
#         serializer = self.serializer_class(queryset, many=False)
#         return Response(serializer.data)
    
#     def create(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         if queryset is None:
#             return Response(status=status.HTTP_403_FORBIDDEN, data={"details": "Profile creation should have been done at the registration level. Seems like that was not done. Something went wrong."})
#         else:
#             serializer = self.get_serializer(queryset, data=request.data, partial=True)
#             serializer.is_valid(raise_exception=True)
#             self.perform_update(serializer)
#             return Response(serializer.data)
