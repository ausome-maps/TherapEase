from rest_framework import permissions


class SubmissionPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ("create", "upload_image"):
            return True
        if view.action in ("list", "retrieve"):
            return request.user.is_authenticated and (
                request.user.is_staff or request.user.is_superuser
            )
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )
