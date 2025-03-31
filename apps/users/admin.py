from django.contrib import admin

from apps.users.models import User, UserTag, Tag

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(UserTag)
