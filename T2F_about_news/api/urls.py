from django.urls import path, include

from djoser.views import UserViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)

from rest_framework.routers import DefaultRouter

from .views import PostViewSets

router = DefaultRouter()
router.register(r'posts', PostViewSets)


urlpatterns = [
    path('auth/signup/', UserViewSet.as_view({'post': 'create'})),
    path('auth/signin/', TokenObtainPairView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),

    path('', include(router.urls)),
]
