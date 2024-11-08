from djoser.serializers import UserCreateSerializer

from django.contrib.auth import get_user_model

from rest_framework import serializers


User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'id', 'username', 'password', 'first_name', 'last_name')
