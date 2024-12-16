from rest_framework import viewsets, status, permissions, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from users.models import User

from .serializers import (
    CustomPasswordSerializer, UserSerializer, AvatarUserSerializer, SelectTagSerializer)


class CustomUserViewSet(viewsets.ModelViewSet):
    """Вьюсет для взаимодейсвия с пользователями."""

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    http_method_names = ['get', 'post']

    def get_permissions(self):
        if self.action == 'me':
            return [permissions.IsAuthenticated(),]
        return [permissions.IsAuthenticatedOrReadOnly(),]

    def get_object(self):
        return self.request.user

    @action(methods=['get'], detail=False,
            permission_classes=[permissions.IsAuthenticated],
            serializer_class=UserSerializer)
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'],
            permission_classes=[permissions.IsAuthenticated],)
    def reset_password(self, request, pk=None):
        user = self.get_object()
        serializer = CustomPasswordSerializer(data=request.data,
                                              context={'request': request})
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'],
            permission_classes=[permissions.IsAuthenticated],
            serializer_class=SelectTagSerializer)
    def select_tag(self, request, pk=None):
        serializer = SelectTagSerializer(data=request.data,
                                         context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AvatarMeUserViewSet(viewsets.GenericViewSet,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin):
    """Вьюсет для взаимодейсвия пользователя со своей аватаркой."""

    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = AvatarUserSerializer

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user.avatar:
            user.avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = AvatarUserSerializer(data=request.data)
        if serializer.is_valid():
            user.avatar = serializer.validated_data['avatar']
            user.save()
            return Response(status=status.HTTP_200_OK)
