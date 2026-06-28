from django.contrib import admin
from .models import FacilitySubmission


class FacilitySubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "placename_display", "submitter_email", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("submitter_email", "submitter_name", "payload")
    readonly_fields = ("created_at", "updated_at", "placename_display")

    def placename_display(self, obj):
        try:
            return obj.payload.get("properties", {}).get("placename", "")
        except (AttributeError, KeyError):
            return ""
    placename_display.short_description = "Placename"


admin.site.register(FacilitySubmission, FacilitySubmissionAdmin)
