from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.users.views import (
    SignUpView, LoginView, MainView, PasswordResetView, ProfileDetailView,
    TagListView, PostListView, NewsListView, NewsDetailView, PostDetailView,
    SettingsView, AboutAuthorView)


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Документация для вашего API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="morozov460336@yandex.ru"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
     path('api/', include('apps.users.urls')),
     path('api/', include('apps.blog.urls')),

     path('admin/', admin.site.urls),

     re_path(r'^swagger(?P<format>\.json|\.yaml)$',
             schema_view.without_ui(cache_timeout=0),
             name='schema-json'),
     path('swagger/',
          schema_view.with_ui('swagger', cache_timeout=0),
          name='schema-swagger-ui'),
     path('redoc/',
          schema_view.with_ui('redoc', cache_timeout=0),
          name='schema-redoc'),

     path('auth/signup/', SignUpView.as_view(), name='signup'),
     path('auth/signin/', LoginView.as_view(), name='signin'),

     path('', MainView.as_view(), name='main'),

     path('password_change/',
          PasswordResetView.as_view(),
          name='change_password'),

     path('tags/',
          TagListView.as_view(),
          name='tag_list'),
     path('posts/',
          PostListView.as_view(),
          name='posts'),
     path('news/',
          NewsListView.as_view(),
          name='news'),
     path('news/<int:pk>/',
          NewsDetailView.as_view(),
          name='news_detail'),
     path('posts/<int:pk>/',
          PostDetailView.as_view(),
          name='post_detail'),

     path('profile/<int:user_id>/',
          ProfileDetailView.as_view(),
          name='profile'),

     path('settings/',
          SettingsView.as_view(),
          name='settings'),

     path('about/',
          AboutAuthorView.as_view(),
          name='about')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
