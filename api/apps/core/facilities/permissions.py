from rest_framework import permissions
from apps.core.users.models import OrganizationRole


class FacilitiesPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["list", "retrieve", "search"]:
            return True
        elif view.action in [
            "update",
            "partial_update",
            "destroy",
            "create",
        ]:
            if not request.user.is_authenticated:
                return False
            return (
                request.user.is_superuser
                or request.user.is_staff
                or OrganizationRole.objects.filter(
                    user=request.user,
                    role__permissions__codename="manage_organization_facilities",
                    status="active",
                ).exists()
            )
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == "retrieve":
            return True
        elif view.action in ["update", "partial_update", "destroy"]:
            if not request.user.is_authenticated:
                return False
            if request.user.is_superuser or request.user.is_staff:
                return True
            return OrganizationRole.objects.filter(
                user=request.user,
                role__permissions__codename="manage_organization_facilities",
                status="active",
            ).exists()
        else:
            return False
