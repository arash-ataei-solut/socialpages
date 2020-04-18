from rest_framework import permissions


class IsSenderOrIsAuthenticatedOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user and request.user.is_authenticated and request.method == 'POST':
            return True
        else:
            return obj.sender == request.user
