from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import PostViewSet, TagViewSet, CommentViewSet, NewsViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'tags', TagViewSet)
router.register(
    r'posts\/(?P<post_id>\d+)\/comments',
    CommentViewSet,
    basename='comments')
router.register(r'news', NewsViewSet, basename='news')


urlpatterns = [
    path('', include(router.urls)),
    path('news/tag/<str:tag>/', NewsViewSet.as_view({'get': 'list'})),
]
