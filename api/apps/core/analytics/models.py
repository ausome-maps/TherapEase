import uuid
from django.db import models


class PageVisit(models.Model):
    """Tracks each page visit to the website."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    path = models.CharField(max_length=500, help_text="URL path visited (e.g., /, /search, /details)")
    referrer = models.CharField(max_length=500, blank=True, default="")
    user_agent = models.TextField(blank=True, default="")
    ip_hash = models.CharField(max_length=64, blank=True, default="", help_text="SHA-256 hash of client IP for privacy")
    session_id = models.CharField(max_length=100, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Page Visit"
        verbose_name_plural = "Page Visits"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["path"]),
            models.Index(fields=["session_id"]),
        ]

    def __str__(self):
        return f"Visit to {self.path} at {self.created_at}"


class FacilityView(models.Model):
    """Tracks when a facility detail page is loaded/viewed."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facility_id = models.CharField(max_length=100, help_text="ID of the facility being viewed")
    facility_name = models.CharField(max_length=500, blank=True, default="")
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        verbose_name = "Facility View"
        verbose_name_plural = "Facility Views"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["-timestamp"]),
            models.Index(fields=["facility_id"]),
            models.Index(fields=["facility_id", "-timestamp"]),
        ]

    def __str__(self):
        return f"Facility {self.facility_id} viewed at {self.timestamp}"


class SearchQuery(models.Model):
    """Tracks search queries executed in the search bar."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    query_text = models.CharField(max_length=500, help_text="The search query text")
    result_count = models.IntegerField(default=0, help_text="Number of results returned")
    filters_applied = models.JSONField(default=dict, blank=True, help_text="Any filters applied with the search")
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        verbose_name = "Search Query"
        verbose_name_plural = "Search Queries"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["-timestamp"]),
            models.Index(fields=["query_text"]),
        ]

    def __str__(self):
        return f"Search '{self.query_text}' at {self.timestamp}"


class AnalyticsArchive(models.Model):
    """Stores archived analytics data as CSV files, attached to weekly reports.

    After each weekly report is generated, the raw analytics rows for that
    week are exported to a CSV, saved here, and then deleted from the live
    tables to save database space.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    week_start = models.DateField(help_text="Start date of the archived week")
    week_end = models.DateField(help_text="End date of the archived week")
    csv_file = models.FileField(upload_to="analytics_archives/", help_text="CSV file containing the archived raw data")
    page_visits_count = models.PositiveIntegerField(default=0)
    facility_views_count = models.PositiveIntegerField(default=0)
    search_queries_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Analytics Archive"
        verbose_name_plural = "Analytics Archives"
        ordering = ["-week_start"]

    def __str__(self):
        return f"Archive {self.week_start} – {self.week_end} ({self.created_at.date()})"


class ReportRecipient(models.Model):
    """Configurable email recipients for the weekly analytics report.

    Managed via Django admin. The weekly task sends the report to all
    active (enabled) recipients.
    """

    email = models.EmailField(unique=True, help_text="Email address to receive the weekly analytics report")
    enabled = models.BooleanField(default=True, help_text="If unchecked, this recipient will not receive reports")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Report Recipient"
        verbose_name_plural = "Report Recipients"
        ordering = ["email"]

    def __str__(self):
        status = "✓" if self.enabled else "✗"
        return f"{status} {self.email}"
