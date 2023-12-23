from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile, Organization, OrganizationRole, Roles


# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"


class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "email",
        "is_superuser",
        "is_staff",
        "is_active",
    )
    inlines = (ProfileInline,)


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "login_count",
        "account_expiry",
        "is_active",
    )
    list_filter = ("user__is_active",)

    @staticmethod
    def is_active(obj):
        return obj.user.is_active


class RoleAdmin(admin.ModelAdmin):
    filter_horizontal = ("permissions",)
    list_display = ("id", "name", "role_type")


class OrganizationAdmin(admin.ModelAdmin):
    filter_horizontal = ("members", "facilities")
    list_display = ("id", "name", "update_date")


class OrganizationRoleAdmin(admin.ModelAdmin):
    raw_id_fields = ("user", "organization")
    list_display = ("id", "organization", "user", "role")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Roles, RoleAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationRole, OrganizationRoleAdmin)
