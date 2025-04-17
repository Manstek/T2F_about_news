from django.urls import path, include

from djoser.views import UserViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)

from rest_framework.routers import DefaultRouter

from apps.users.views import CustomUserViewSet, AvatarMeUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)


urlpatterns = [
    path('auth/signup/', UserViewSet.as_view({'post': 'create'})),
    path('auth/signin/', TokenObtainPairView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),

    path('users/me/avatar/', AvatarMeUserViewSet.as_view({
        'delete': 'destroy', 'put': 'update'})),

    path('', include(router.urls)),
]
