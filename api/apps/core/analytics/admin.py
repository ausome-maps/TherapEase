import logging

from django.contrib import admin, messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path
from django.utils import timezone

logger = logging.getLogger(__name__)

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
    list_display = [
        "week_start",
        "week_end",
        "page_visits_count",
        "facility_views_count",
        "search_queries_count",
        "created_at",
    ]
    list_filter = ["week_start"]
    readonly_fields = ["id", "csv_file", "created_at"]
    ordering = ["-week_start"]

    # ── Custom admin views ─────────────────────────────────────────

    change_list_template = "admin/analytics/analyticsarchive_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "send-report/",
                self.admin_site.admin_view(self.send_report_view),
                name="analytics-analyticsarchive-send-report",
            ),
        ]
        return custom_urls + urls

    def send_report_view(self, request):
        """Admin view that triggers a report-only send (no archive, no deletion)."""
        if request.method == "POST":
            from .tasks import send_report_only

            week_start_str = request.POST.get("week_start", "") or None

            # Try celery first; fall back to synchronous if broker is unreachable
            try:
                result = send_report_only.delay(week_start_str=week_start_str)
                self.message_user(
                    request,
                    f"Report queued (task {result.id}). It will be sent to all enabled recipients shortly.",
                    messages.SUCCESS,
                )
            except Exception:
                # Broker unreachable → run inline
                logger.warning("Celery broker unreachable, sending report synchronously.")
                try:
                    outcome = send_report_only(week_start_str=week_start_str)
                    self.message_user(
                        request,
                        f"Report sent! Visits: {outcome['total_visits']}, "
                        f"Facility views: {outcome['total_facility_views']}, "
                        f"Searches: {outcome['total_searches']}.",
                        messages.SUCCESS,
                    )
                except Exception as exc:
                    self.message_user(
                        request,
                        f"Failed to send report: {exc}",
                        messages.ERROR,
                    )

            return redirect("admin:analytics_analyticsarchive_changelist")

        # GET → show confirmation page
        context = {
            **self.admin_site.each_context(request),
            "title": "Send analytics report",
            "opts": self.model._meta,
            "today": timezone.now().date().isoformat(),
        }
        return TemplateResponse(request, "admin/analytics/send_report_confirm.html", context)


@admin.register(ReportRecipient)
class ReportRecipientAdmin(admin.ModelAdmin):
    list_display = ["email", "enabled", "created_at"]
    list_filter = ["enabled"]
    search_fields = ["email"]
    ordering = ["email"]
