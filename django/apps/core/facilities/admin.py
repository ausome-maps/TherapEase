from django.contrib import admin
from .models import Facilities, FacilityProperties


class FacilityPropertiesAdmin(admin.ModelAdmin):
    list_display = ("osm_id", "placename", "city", "region")
    list_filter = ("city", "region")


class FacilitiesAdmin(admin.ModelAdmin):
    list_display = ("id", "placename", "city", "region")
    list_filter = ("properties__city", "properties__region")

    def placename(self, obj):
        return obj.properties.placename

    def city(self, obj):
        return obj.properties.city

    def region(self, obj):
        return obj.properties.region


admin.site.register(Facilities, FacilitiesAdmin)
admin.site.register(FacilityProperties, FacilityPropertiesAdmin)
