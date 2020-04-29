from rest_framework import permissions

from .models import Post


class IsSenderOrIsAuthenticatedOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        pk = request.path.split(sep='/')[2]
        if pk.isdecimal():
            instance = Post.objects.filter(pk=pk).select_related('sender')
            if instance[0] and instance[0].sender == request.user:
                return True
        else:
            return False
