from django.urls import path, include


urlpatterns = [
    path('auth/', include('api.users.urls')),
    path('', include('api.blog.urls')),
]
