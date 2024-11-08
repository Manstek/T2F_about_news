from django.urls import path

from djoser.views import TokenCreateView, UserViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)


urlpatterns = [
    path('auth/SignUp/', UserViewSet.as_view({'post': 'create'})),
    path('auth/SignIn/', TokenObtainPairView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
]
