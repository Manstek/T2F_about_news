from djoser.serializers import UserCreateSerializer

from django.contrib.auth import get_user_model

from rest_framework import serializers


User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'id', 'username', 'password', 'first_name', 'last_name')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра своего профиля."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'tags', 'avatar')


class CustomPasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля."""

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Текущий пароль указан неверно.')
        return value


class AvatarUserSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с аватаром пользователя."""

    class Meta:
        model = User
        fields = ('avatar',)
