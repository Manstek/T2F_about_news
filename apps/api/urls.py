from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.api.users.views import CustomUserViewSet, AvatarMeUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)


urlpatterns = [
    path('users/me/avatar/', AvatarMeUserViewSet.as_view({
        'delete': 'destroy', 'put': 'update'})),

    path('auth/', include('apps.api.users.urls')),

    path('', include('apps.api.blog.urls')),
    path('', include(router.urls))
]
