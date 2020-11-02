from rest_framework import permissions
from .models import Poem

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsPoemOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        poem_owner = Poem.objects.get(id=obj.poem_n).owner
        return obj.owner == request.user or poem_owner == request.user
