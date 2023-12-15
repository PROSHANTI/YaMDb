from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed


class AdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_admin
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
            or request.user.is_staff
        )


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(IsAdmin):

    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            or request.method in permissions.SAFE_METHODS
        )


class AuthorModerAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'PUT':
            raise MethodNotAllowed('Метод PUT не предусмотрен.')
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return (
                request.user.is_admin
                or request.user.is_moderator
                or (request.user == obj.author)
            )
        return True
