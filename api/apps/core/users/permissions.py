from django.contrib.auth.models import User
from rest_framework import permissions
from .models import OrganizationRole

class OrganizationPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ["list", "retrieve", "search"]:
            return True
        elif view.action in [
            "update",
            "partial_update",
            "destroy",
            "create",
        ]:
            return request.user.user_org_role.filter(role__permissions__codename="manage_organization").exists() or request.user.is_staff
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == "retrieve":
            return True
        elif view.action in ["update", "partial_update"]:
            if OrganizationRole.objects.filter(organization=obj, user=request.user).exists():
                return True
            return False
        else:
            return False
