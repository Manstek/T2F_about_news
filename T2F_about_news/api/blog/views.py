from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, mixins

from blog.models import Post, News

from users.models import Tag

from .serializers import (
    PostSerializer, TagSerializer, CommentSerializer, NewsSerializer)
from .permissions import IsAuthorOrAdmin, IsAdmin


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с постами."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'delete', 'patch']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""

    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'delete', 'patch']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        post=get_object_or_404(Post, pk=self.kwargs['post_id']))

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

    serializer_class = NewsSerializer
    http_method_names = ['get']

    def get_queryset(self):
        tag_name = self.kwargs.get('tag')
        if tag_name:
            return News.objects.filter(tags__name=tag_name)
        return News.objects.all()
