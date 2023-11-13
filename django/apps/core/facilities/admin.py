from django.contrib import admin
from .models import Facilities, FacilityProperties


class FacilityPropertiesAdmin(admin.ModelAdmin):
    list_display = ("id", "placename", "city", "region")
    list_filter = ("city", "region")


class FacilitiesAdmin(admin.ModelAdmin):
    list_display = ("id", "placename", "geometry")

    def placename(self, obj):
        return obj.properties.placename


admin.site.register(Facilities, FacilitiesAdmin)
admin.site.register(FacilityProperties, FacilityPropertiesAdmin)
