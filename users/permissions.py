from typing import Optional

from django.contrib.auth.models import User
from rest_framework import permissions


class UserRegistrationOrThemselfOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Optional[User]):
        if request.method in permissions.SAFE_METHODS:
            return True
        # registration allowed only for unauthenticated users
        if request.method == 'POST':
            return request.user is None
        # or themself
        return obj == request.user
