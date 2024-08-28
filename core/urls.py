from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, PasswordResetView, PasswordResetConfirmView

router = DefaultRouter()
router.register('', UserViewSet, basename='settings')

urlpatterns = [
    path('users/reset_password/', PasswordResetView.as_view(), name='password_reset'),
    path('users/reset_password_confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('', include(router.urls)),
]
