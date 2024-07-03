from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Moderator').exists()

    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='Moderator').exists()
