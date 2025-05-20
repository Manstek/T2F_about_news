from rest_framework import serializers

from apps.users.serializers import Base64ImageField, UserSerializer

from apps.blog.models import Post, Comment, News, ShortNews

from apps.users.models import Tag


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для постов."""

    image = Base64ImageField(required=False)
    author = UserSerializer()

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'text', 'pub_date', 'image')


class PostCreateSerializer(PostSerializer):
    """Сериализатор для создания постов."""

    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'author', 'text', 'image')


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


class ShortNewsListSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения сжатых новостей."""

    tag = serializers.CharField(source='news.tag.name')
    source = serializers.CharField(source='news.source')
    news_url = serializers.URLField(source='news.news_url')
    image_url = serializers.URLField(source='news.image_url')
    pub_date = serializers.DateTimeField(source='news.pub_date')

    class Meta:
        model = ShortNews
        fields = ('id', 'text', 'tag', 'source', 'image_url', 'news_url',
                  'pub_date')
