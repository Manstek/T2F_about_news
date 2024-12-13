from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.users.views import CustomUserViewSet, AvatarMeUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)


urlpatterns = [
    path('users/me/avatar/', AvatarMeUserViewSet.as_view({
        'delete': 'destroy', 'put': 'update'})),
    path('auth/', include('api.users.urls')),
    path('', include('api.blog.urls')),
    path('', include(router.urls))
]
