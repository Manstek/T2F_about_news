from django.contrib import admin

from apps.blog.models import Post, Comment, News, ShortNews

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(News)
admin.site.register(ShortNews)
