from django.urls import include, path
from rest_framework.routers import SimpleRouter
from . import views


router2 = SimpleRouter()
router2.register('', views.TopicListCreateAPIView, basename='topic_view_set')

router = SimpleRouter()
router.register('', views.UserViewSet, basename='user_view_set')

urlpatterns = [
    # path('space-host/', views.SpaceHostListCreateAPIView.as_view(), name='space_host_list'),
    path('topics/', include(router2.urls)),
    path('', include(router.urls)),
]