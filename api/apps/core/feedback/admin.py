from django.contrib import admin
from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "facility", "email_address", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = (
        "email_address",
        "contact_number",
        "data_concerns",
        "usability_concerns",
        "admin_notes",
    )
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Feedback, FeedbackAdmin)
