from rest_framework import permissions


class AnonPermissionOnly(permissions.BasePermission):
    # non auth only
    message = "You are authenticated"
    def has_permission(self, request, view):
        return not request.user.is_authenticated

        