from rest_framework import permissions


def is_owner(user):
    return user.groups.filter(name='OWNER').exists()


def is_driver(user):
    return user.groups.filter(name='DRIVER').exists()


class IsOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_owner(request.user)


class IsDriverPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_driver(request.user)


class IsOwnerOrDriverPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return is_driver(request.user) or is_owner(request.user)