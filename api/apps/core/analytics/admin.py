from django.contrib import admin
from .models import AnalyticsArchive, FacilityView, PageVisit, ReportRecipient, SearchQuery


@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ["path", "session_id", "created_at"]
    list_filter = ["path", "created_at"]
    search_fields = ["path", "session_id"]
    date_hierarchy = "created_at"
    readonly_fields = ["id", "created_at"]


@admin.register(FacilityView)
class FacilityViewAdmin(admin.ModelAdmin):
    list_display = ["facility_id", "facility_name", "timestamp"]
    list_filter = ["timestamp"]
    search_fields = ["facility_id", "facility_name"]
    date_hierarchy = "timestamp"
    readonly_fields = ["id", "timestamp"]


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ["query_text", "result_count", "timestamp"]
    list_filter = ["timestamp"]
    search_fields = ["query_text"]
    date_hierarchy = "timestamp"
    readonly_fields = ["id", "timestamp"]


@admin.register(AnalyticsArchive)
class AnalyticsArchiveAdmin(admin.ModelAdmin):
    list_display = ["week_start", "week_end", "page_visits_count", "facility_views_count", "search_queries_count", "created_at"]
    list_filter = ["week_start"]
    readonly_fields = ["id", "csv_file", "created_at"]
    ordering = ["-week_start"]


@admin.register(ReportRecipient)
class ReportRecipientAdmin(admin.ModelAdmin):
    list_display = ["email", "enabled", "created_at"]
    list_filter = ["enabled"]
    search_fields = ["email"]
    ordering = ["email"]
