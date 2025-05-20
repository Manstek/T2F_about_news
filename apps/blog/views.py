from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.blog.models import Post, News, ShortNews

from apps.users.models import Tag

from apps.blog.serializers import (
    PostSerializer, TagSerializer, CommentSerializer, ShortNewsListSerializer,
    PostCreateSerializer)
from apps.blog.permissions import IsAuthorOrAdmin, IsAdmin


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с постами."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'delete', 'patch']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return super().get_serializer_class()


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""

    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'delete', 'patch']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        post=get_object_or_404(Post,
                                               pk=self.kwargs['post_id']))

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return post.comments.all()

    def get_permissions(self):
        if self.action in ('destroy', 'partial_update'):
            return (IsAuthorOrAdmin(),)
        return super().get_permissions()


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Вьюсет для работы с тегами."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdmin(), ]
        return super().get_permissions()


class NewsViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с новостями."""

    serializer_class = ShortNewsListSerializer
    http_method_names = ['get']
    queryset = ShortNews.objects.all()

    @action(detail=False, methods=['get'], url_path='my')
    def my_news(self, request):
        """Возвращает сжатые новости по тегам текущего пользователя."""
        user_tags = request.user.tags.all()

        if not user_tags.exists():
            return Response([])

        short_news = ShortNews.objects.filter(
            news__tag__in=user_tags).select_related(
                'news', 'news__tag').distinct()

        serializer = ShortNewsListSerializer(short_news, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='short')
    def short_news(self, request):
        """Возвращает список сжатых новостей с основными данными из News."""
        short_news = ShortNews.objects.select_related('news').all()
        serializer = ShortNewsListSerializer(short_news, many=True)
        return Response(serializer.data)
