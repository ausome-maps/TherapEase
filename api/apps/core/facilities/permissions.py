from rest_framework import permissions


class FacilitiesPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        print(view.action)
        if view.action in ["list", "retrieve", "search"]:
            return True
        elif view.action in [
            "retrieve",
            "update",
            "partial_update",
            "destroy",
            "create",
        ]:
            return request.user.is_superuser
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == "retrieve":
            return True
        elif view.action in ["update", "partial_update", "destroy"]:
            return obj == request.user or request.user.is_superuser
        else:
            return False
