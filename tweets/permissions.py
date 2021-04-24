from rest_framework import permissions

from tweets.models import Tweet


class IsAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj: Tweet):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
