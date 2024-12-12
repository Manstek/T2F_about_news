from rest_framework import viewsets, permissions

from blog.models import Post

from .blog.serializers import PostSerializer
from .blog.permissions import IsAuthorOrAdmin


class PostViewSets(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrAdmin]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
