from rest_framework import permissions


class FeedbackPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "create":
            return True
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )
