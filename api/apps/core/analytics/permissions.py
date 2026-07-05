from rest_framework import permissions


class AnalyticsPermissions(permissions.BasePermission):
    """Allow any client to create analytics events; restrict reads to staff/superusers."""

    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )
