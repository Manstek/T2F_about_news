from rest_framework import viewsets, permissions, mixins

from blog.models import Post

from users.models import Tag

from .serializers import PostSerializer, TagSerializer
from .permissions import IsAuthorOrAdmin, IsAdmin


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrAdmin]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdmin(), ]
        return super().get_permissions()
