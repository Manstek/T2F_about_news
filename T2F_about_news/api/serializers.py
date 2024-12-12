from djoser.serializers import UserCreateSerializer

from django.contrib.auth import get_user_model

from rest_framework import serializers

from blog.models import Post


User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'id', 'username', 'password', 'first_name', 'last_name')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'text', 'pub_date')
        # read_only = ('author',)
