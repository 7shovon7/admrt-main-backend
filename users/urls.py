from django.urls import include, path
from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter()
router.register('', views.UserViewSet, basename='user_view_set')


urlpatterns = [
    # path('space-host/', views.SpaceHostListCreateAPIView.as_view(), name='space_host_list'),
    path('', include(router.urls)),
]