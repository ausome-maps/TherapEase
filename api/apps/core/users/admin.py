from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile


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


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
