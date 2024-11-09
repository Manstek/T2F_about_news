from rest_framework import viewsets, permissions

from .serializers import PostSerializer
from .permissions import IsAuthorOrAdmin

from core.models import Post


class PostViewSets(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrAdmin]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
