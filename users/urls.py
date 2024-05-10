from django.urls import include, path
from rest_framework.routers import SimpleRouter
from . import views


product_router = SimpleRouter()
product_router.register('', views.AdvertiserProductViewSet, basename='product_view_set')

social_router = SimpleRouter()
social_router.register('', views.SocialMediaViewSet, basename='social_view_set')

portfolio_router = SimpleRouter()
portfolio_router.register('', views.PortfolioViewSet, basename='portfolio_view_set')

portfolio_images_router = SimpleRouter()
portfolio_images_router.register('', views.PortfolioImageViewSet, basename='portfolio_images_view_set')

language_router = SimpleRouter()
language_router.register('', views.LanguageViewSet, basename='language_view_set')

topic_router = SimpleRouter()
topic_router.register('', views.TopicViewSet, basename='topic_view_set')

router = SimpleRouter()
router.register('', views.UserViewSet, basename='user_view_set')

urlpatterns = [
    path('products/', include(product_router.urls)),
    path('socials/', include(social_router.urls)),
    path('portfolios/<int:id>/images/', include(portfolio_images_router.urls)),
    path('portfolios/', include(portfolio_router.urls)),
    path('languages/', include(language_router.urls)),
    path('topics/', include(topic_router.urls)),
    path('', include(router.urls)),
]