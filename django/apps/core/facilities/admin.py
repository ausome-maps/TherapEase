from django.contrib import admin
from .models import Facilities, FacilityProperties


class FacilityPropertiesAdmin(admin.ModelAdmin):
    list_display = ("osm_id", "placename", "city", "region")
    list_filter = ("city", "region")
    search_fields = ("city", "placename", "region", "address")


class FacilitiesAdmin(admin.ModelAdmin):
    list_display = ("id", "placename", "city", "region")
    list_filter = ("properties__city", "properties__region")
    search_fields = ("properties__city", "properties__placename", "properties__region", "properties__address")

    def placename(self, obj):
        return obj.properties.placename

    def city(self, obj):
        return obj.properties.city

    def region(self, obj):
        return obj.properties.region


admin.site.register(Facilities, FacilitiesAdmin)
admin.site.register(FacilityProperties, FacilityPropertiesAdmin)
