from django.urls import path

from djoser.views import UserViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)


urlpatterns = [
    path('signup/', UserViewSet.as_view({'post': 'create'})),
    path('signin/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
