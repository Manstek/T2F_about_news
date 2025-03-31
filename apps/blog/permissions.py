from rest_framework import permissions


class IsAuthorOrAdmin(permissions.BasePermission):
    """Является ли пользователь администратором, или владельцем."""

    def has_object_permission(self, request, view, obj):
        print(obj)
        return request.user.is_superuser or request.user == obj.author


class IsAdmin(permissions.BasePermission):
    """Является ли пользователь администратором."""

    def has_permission(self, request, view):
        return request.user.is_superuser
