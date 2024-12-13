from rest_framework import serializers

from blog.models import Post

from users.models import Tag


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для постов."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'text', 'pub_date')
        # read_only = ('author',)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = ('__all__')
