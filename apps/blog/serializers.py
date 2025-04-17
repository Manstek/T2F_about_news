from rest_framework import serializers

from apps.users.serializers import Base64ImageField

from apps.blog.models import Post, Comment, News

from apps.users.models import Tag


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для постов."""

    author = serializers.StringRelatedField(read_only=True)
    image = Base64ImageField(required=False)

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'text', 'pub_date', 'image')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = ('__all__')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    class Meta:
        model = Comment
        fields = ('id', 'text', 'pub_date')


class NewsSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения новостей."""

    tag = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = News
        fields = '__all__'
