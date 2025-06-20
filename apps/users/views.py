from rest_framework import viewsets, status, permissions, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.users.models import User

from apps.users.serializers import (
    CustomPasswordSerializer, UserSerializer,
    AvatarUserSerializer, SelectTagSerializer)

from django.shortcuts import render
from django.views import View


class CustomUserViewSet(viewsets.ModelViewSet):
    """Вьюсет для взаимодейсвия с пользователями."""

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch']

    def get_permissions(self):
        if self.action == 'me':
            return [permissions.IsAuthenticated(),]
        return [permissions.IsAuthenticatedOrReadOnly(),]

    def get_object(self):
        if self.action == 'me':
            return self.request.user
        return super().get_object()

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

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
        user = request.user
        serializer = SelectTagSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            new_tags = serializer.validated_data['tag']

            user.tags.clear()
            user.tags.add(*new_tags)

            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        return Response(serializer.errors)


class SignUpView(View):
    def get(self, request):
        return render(request, 'auth/signup.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'auth/signin.html')


class MainView(View):
    def get(self, request):
        return render(request, 'index.html')


class PasswordResetView(View):
    def get(self, request):
        return render(request, 'users/password_change.html')


class TagListView(View):
    def get(self, request):
        return render(request, 'users/tag_list.html')


class PostListView(View):
    def get(self, request):
        return render(request, 'blog/posts.html')


class NewsListView(View):
    def get(self, request):
        return render(request, 'blog/news.html')


class NewsDetailView(View):
    def get(self, request, pk):
        return render(request, 'blog/news_detail.html')


class PostDetailView(View):
    def get(self, request, pk):
        return render(request, 'blog/post_detail.html')


class ProfileDetailView(View):
    def get(self, request, user_id):
        return render(request, 'users/profile.html')


class SettingsView(View):
    def get(self, request):
        return render(request, 'users/settings.html')


class AboutAuthorView(View):
    def get(self, request):
        return render(request, 'includes/about.html')
