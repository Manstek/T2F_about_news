from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from apps.blog.models import Post, ShortNews

from apps.users.models import Tag, User

from apps.blog.serializers import (
    PostSerializer, TagSerializer, CommentSerializer, ShortNewsListSerializer,
    PostCreateSerializer, CommentCreateSerializer)
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

    def get_queryset(self):
        return Post.objects.annotate(
            comments_count=Count('comments')).order_by('-pub_date')

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>[^/.]+)')
    def user_posts(self, request, user_id=None):
        """Возвращает список Постов текущего пользователя."""
        user = get_object_or_404(User, id=user_id)
        posts = Post.objects.filter(author=user).all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


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

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return super().get_serializer_class()


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
    pagination_class = LimitOffsetPagination

    @action(detail=False, methods=['get'], url_path='my')
    def my_news(self, request):
        user_tags = request.user.tags.all()
        if not user_tags.exists():
            return Response([])

        short_news = ShortNews.objects.filter(
            news__tag__in=user_tags
        ).select_related('news', 'news__tag').order_by('-news__pub_date').distinct()

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(short_news, request, view=self)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(short_news, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='short')
    def short_news(self, request):
        """Возвращает список сжатых новостей с основными данными из News."""
        short_news = ShortNews.objects.select_related(
            'news').order_by('-news__pub_date').all()
        serializer = ShortNewsListSerializer(short_news, many=True)
        return Response(serializer.data)
