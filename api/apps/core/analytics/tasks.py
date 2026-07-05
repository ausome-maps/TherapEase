import csv
import io
import os
import tempfile
from datetime import datetime, timedelta

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.template.loader import get_template
from django.utils import timezone

from .models import AnalyticsArchive, FacilityView, PageVisit, ReportRecipient, SearchQuery
from .utils import is_bot

logger = get_task_logger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_report_context(week_ago: datetime, now: datetime) -> dict:
    """Query the live tables and return the template context dict."""

    # Page visits
    total_visits = PageVisit.objects.filter(created_at__gte=week_ago).count()
    visits_by_day = (
        PageVisit.objects.filter(created_at__gte=week_ago)
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )
    top_pages = (
        PageVisit.objects.filter(created_at__gte=week_ago)
        .values("path")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )
    unique_sessions = (
        PageVisit.objects.filter(created_at__gte=week_ago)
        .exclude(session_id="")
        .values("session_id")
        .distinct()
        .count()
    )

    # Facility views
    total_facility_views = FacilityView.objects.filter(timestamp__gte=week_ago).count()
    facility_views_by_day = (
        FacilityView.objects.filter(timestamp__gte=week_ago)
        .annotate(day=TruncDate("timestamp"))
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )
    top_facilities = (
        FacilityView.objects.filter(timestamp__gte=week_ago)
        .values("facility_id", "facility_name")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    # Search queries
    total_searches = SearchQuery.objects.filter(timestamp__gte=week_ago).count()
    searches_by_day = (
        SearchQuery.objects.filter(timestamp__gte=week_ago)
        .annotate(day=TruncDate("timestamp"))
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )
    top_searches = (
        SearchQuery.objects.filter(timestamp__gte=week_ago)
        .values("query_text")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    return {
        "week_start": week_ago.strftime("%B %d, %Y"),
        "week_end": now.strftime("%B %d, %Y"),
        "total_visits": total_visits,
        "unique_sessions": unique_sessions,
        "visits_by_day": visits_by_day,
        "top_pages": top_pages,
        "total_facility_views": total_facility_views,
        "facility_views_by_day": facility_views_by_day,
        "top_facilities": top_facilities,
        "total_searches": total_searches,
        "searches_by_day": searches_by_day,
        "top_searches": top_searches,
        "site_name": settings.SITE_NAME,
    }


def _export_week_to_csv(week_start: datetime, week_end: datetime) -> tuple[io.BytesIO, int, int, int]:
    """Export raw analytics rows for *week_start .. week_end* into an
    in-memory CSV file.

    Returns ``(csv_buffer, pv_count, fv_count, sq_count)``.
    """
    csv_buffer = io.BytesIO()
    # Use a TextIOWrapper so the csv module can write str
    text_wrapper = io.TextIOWrapper(csv_buffer, encoding="utf-8", newline="")
    writer = csv.writer(text_wrapper)

    # Header
    writer.writerow([
        "type",
        "timestamp",
        "path",
        "referrer",
        "user_agent",
        "ip_hash",
        "facility_id",
        "facility_name",
        "query_text",
        "result_count",
        "filters_applied",
        "session_id",
    ])

    pv_count = 0
    fv_count = 0
    sq_count = 0

    # ---- PageVisits -------------------------------------------------------
    pv_qs = PageVisit.objects.filter(created_at__gte=week_start, created_at__lt=week_end)
    pv_count = pv_qs.count()
    for pv in pv_qs.iterator(chunk_size=2000):
        writer.writerow([
            "page_visit",
            pv.created_at.isoformat(),
            pv.path,
            pv.referrer,
            pv.user_agent,
            pv.ip_hash,
            "",  # facility_id
            "",  # facility_name
            "",  # query_text
            "",  # result_count
            "",  # filters_applied
            pv.session_id,
        ])

    # ---- FacilityViews ----------------------------------------------------
    fv_qs = FacilityView.objects.filter(timestamp__gte=week_start, timestamp__lt=week_end)
    fv_count = fv_qs.count()
    for fv in fv_qs.iterator(chunk_size=2000):
        writer.writerow([
            "facility_view",
            fv.timestamp.isoformat(),
            "",  # path
            "",  # referrer
            "",  # user_agent
            "",  # ip_hash
            fv.facility_id,
            fv.facility_name,
            "",  # query_text
            "",  # result_count
            "",  # filters_applied
            fv.session_id,
        ])

    # ---- SearchQueries ----------------------------------------------------
    sq_qs = SearchQuery.objects.filter(timestamp__gte=week_start, timestamp__lt=week_end)
    sq_count = sq_qs.count()
    for sq in sq_qs.iterator(chunk_size=2000):
        writer.writerow([
            "search_query",
            sq.timestamp.isoformat(),
            "",  # path
            "",  # referrer
            "",  # user_agent
            "",  # ip_hash
            "",  # facility_id
            "",  # facility_name
            sq.query_text,
            sq.result_count,
            sq.filters_applied,
            sq.session_id,
        ])

    # Flush the TextIOWrapper so all bytes are written to the underlying buffer
    text_wrapper.detach()
    csv_buffer.seek(0)
    return csv_buffer, pv_count, fv_count, sq_count


def _delete_week_rows(week_start: datetime, week_end: datetime) -> tuple[int, int, int]:
    """Delete raw analytics rows for the given week range.

    Returns ``(pv_deleted, fv_deleted, sq_deleted)``.
    """
    pv_deleted, _ = PageVisit.objects.filter(
        created_at__gte=week_start, created_at__lt=week_end
    ).delete()
    fv_deleted, _ = FacilityView.objects.filter(
        timestamp__gte=week_start, timestamp__lt=week_end
    ).delete()
    sq_deleted, _ = SearchQuery.objects.filter(
        timestamp__gte=week_start, timestamp__lt=week_end
    ).delete()
    return pv_deleted, fv_deleted, sq_deleted


# ---------------------------------------------------------------------------
# Celery tasks
# ---------------------------------------------------------------------------

@shared_task
def archive_analytics_week(week_start_str: str | None = None) -> dict | None:
    """Archive (export → CSV → delete) analytics data for a given week.

    If *week_start_str* is ``None``, the task archives the **penultimate**
    completed week (i.e. the week before last).  This guarantees that the
    current week's data is never touched while it may still be receiving
    events.

    The CSV is saved as an ``AnalyticsArchive`` record so it can be
    attached to the weekly report email or downloaded later.
    """
    now = timezone.now()

    if week_start_str:
        week_start = datetime.strptime(week_start_str, "%Y-%m-%d").date()
    else:
        # Default: archive the week that ended last Sunday
        days_since_monday = now.weekday()  # Monday=0 … Sunday=6
        last_monday = (now - timedelta(days=days_since_monday + 7)).date()
        week_start = last_monday

    week_end = week_start + timedelta(days=7)

    week_start_dt = timezone.make_aware(
        datetime.combine(week_start, datetime.min.time())
    )
    week_end_dt = timezone.make_aware(
        datetime.combine(week_end, datetime.min.time())
    )

    # 1. Export raw rows to an in-memory CSV
    csv_buffer, pv_count, fv_count, sq_count = _export_week_to_csv(
        week_start_dt, week_end_dt
    )

    if pv_count == 0 and fv_count == 0 and sq_count == 0:
        logger.info("No analytics data to archive for %s – %s", week_start, week_end)
        return None

    # 2. Save CSV as an AnalyticsArchive record
    filename = f"analytics_{week_start.isoformat()}_{week_end.isoformat()}.csv"
    archive = AnalyticsArchive(
        week_start=week_start,
        week_end=week_end,
        page_visits_count=pv_count,
        facility_views_count=fv_count,
        search_queries_count=sq_count,
    )
    archive.csv_file.save(filename, ContentFile(csv_buffer.read()), save=True)
    csv_buffer.close()

    # 3. Delete the now-archived rows from live tables
    pv_del, fv_del, sq_del = _delete_week_rows(week_start_dt, week_end_dt)

    logger.info(
        "Archived analytics week %s – %s: "
        "PV=%d/%d  FV=%d/%d  SQ=%d/%d  → %s",
        week_start,
        week_end,
        pv_count,
        pv_del,
        fv_count,
        fv_del,
        sq_count,
        sq_del,
        archive.csv_file.url if archive.csv_file else "no-file",
    )

    return {
        "archive_id": str(archive.id),
        "week_start": week_start.isoformat(),
        "week_end": week_end.isoformat(),
        "page_visits": pv_count,
        "facility_views": fv_count,
        "search_queries": sq_count,
        "csv_url": archive.csv_file.url if archive.csv_file else None,
    }


@shared_task
def send_weekly_analytics_report():
    """Send the weekly analytics report email.

    The workflow is:

    1. Archive **last week's** raw data to a CSV (so it is saved before
       it gets summarized).  The archive CSV is attached to the email.
    2. Build the summary report from the (now-archived) live tables.
    3. Send the email with the CSV attachment.
    """
    now = timezone.now()
    # The week being reported on: Mon 00:00 – Sun 23:59 of the previous week
    days_since_monday = now.weekday()  # Monday=0
    report_monday = (now - timedelta(days=days_since_monday + 7)).date()
    report_sunday = report_monday + timedelta(days=6)

    week_ago = timezone.make_aware(
        datetime.combine(report_monday, datetime.min.time())
    )
    week_end = timezone.make_aware(
        datetime.combine(report_sunday, datetime.max.time())
    )

    # 1. Archive last week's raw data → returns the AnalyticsArchive pk
    archive_result = archive_analytics_week(week_start_str=report_monday.isoformat())
    archive_file_path = None
    archive_filename = None

    if archive_result and archive_result.get("archive_id"):
        try:
            archive = AnalyticsArchive.objects.get(id=archive_result["archive_id"])
            if archive.csv_file:
                archive_file_path = archive.csv_file.path
                archive_filename = os.path.basename(archive.csv_file.name)
        except AnalyticsArchive.DoesNotExist:
            logger.warning("Archive record %s not found", archive_result["archive_id"])

    # 2. Build report context
    context = _build_report_context(week_ago, now)

    text_content = get_template("email/analytics_weekly_report.txt").render(context)
    html_content = get_template("email/analytics_weekly_report.html").render(context)

    subject = (
        f"[{settings.SITE_NAME}] Weekly Analytics Report: "
        f"{report_monday.strftime('%b %d')} – {report_sunday.strftime('%b %d, %Y')}"
    )
    from_email = settings.DEFAULT_FROM_EMAIL

    recipients = list(
        ReportRecipient.objects.filter(enabled=True).values_list("email", flat=True)
    )
    if not recipients:
        recipients = [settings.DEFAULT_FROM_EMAIL]

    # 3. Send email (with CSV attachment if available)
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipients)
    msg.attach_alternative(html_content, "text/html")

    if archive_file_path and os.path.isfile(archive_file_path):
        with open(archive_file_path, "rb") as f:
            msg.attach(archive_filename, f.read(), "text/csv")

    msg.send()

    logger.info(
        "Weekly analytics report sent. Visits: %d, Facility views: %d, Searches: %d",
        context["total_visits"],
        context["total_facility_views"],
        context["total_searches"],
    )
    return {
        "total_visits": context["total_visits"],
        "total_facility_views": context["total_facility_views"],
        "total_searches": context["total_searches"],
        "archive_id": archive_result.get("archive_id") if archive_result else None,
    }


@shared_task
def send_report_only(week_start_str: str | None = None) -> dict:
    """Send the weekly analytics report email **without** archiving data.

    Unlike ``send_weekly_analytics_report``, this task does **not** export
    a CSV, does **not** create an AnalyticsArchive record, and does **not**
    delete any rows from the live tables.  It simply builds the summary
    and emails it to the configured recipients.

    If *week_start_str* is ``None``, defaults to the previous calendar week.
    """
    now = timezone.now()

    if week_start_str:
        report_monday = datetime.strptime(week_start_str, "%Y-%m-%d").date()
    else:
        days_since_monday = now.weekday()
        report_monday = (now - timedelta(days=days_since_monday + 7)).date()

    report_sunday = report_monday + timedelta(days=6)

    week_ago = timezone.make_aware(
        datetime.combine(report_monday, datetime.min.time())
    )
    week_end = timezone.make_aware(
        datetime.combine(report_sunday, datetime.max.time())
    )

    context = _build_report_context(week_ago, now)

    text_content = get_template("email/analytics_weekly_report.txt").render(context)
    html_content = get_template("email/analytics_weekly_report.html").render(context)

    subject = (
        f"[{settings.SITE_NAME}] Weekly Analytics Report: "
        f"{report_monday.strftime('%b %d')} – {report_sunday.strftime('%b %d, %Y')}"
    )
    from_email = settings.DEFAULT_FROM_EMAIL

    recipients = list(
        ReportRecipient.objects.filter(enabled=True).values_list("email", flat=True)
    )
    if not recipients:
        recipients = [settings.DEFAULT_FROM_EMAIL]

    msg = EmailMultiAlternatives(subject, text_content, from_email, recipients)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    logger.info(
        "Report-only sent (no archive). Visits: %d, Facility views: %d, Searches: %d",
        context["total_visits"],
        context["total_facility_views"],
        context["total_searches"],
    )
    return {
        "total_visits": context["total_visits"],
        "total_facility_views": context["total_facility_views"],
        "total_searches": context["total_searches"],
        "week_start": report_monday.isoformat(),
        "week_end": report_sunday.isoformat(),
    }


@shared_task
def cleanup_bot_analytics() -> dict:
    """Scan all analytics tables and delete rows from known bots/crawlers.

    Scheduled to run daily.  Deletes records where ``user_agent`` matches
    bot patterns.  FacilityView and SearchQuery rows are joined via
    ``session_id`` to PageVisit to infer bot status for rows that don't
    carry their own user-agent.
    """

    # ── PageVisit ───────────────────────────────────────────────────
    pv_qs = PageVisit.objects.all()
    pv_bot_ids: list[str] = []
    for pv in pv_qs.iterator(chunk_size=2000):
        if is_bot(pv.user_agent):
            pv_bot_ids.append(str(pv.id))

    pv_deleted = 0
    if pv_bot_ids:
        pv_deleted, _ = PageVisit.objects.filter(id__in=pv_bot_ids).delete()

    # ── FacilityView ────────────────────────────────────────────────
    # Join via session_id to find bot-associated facility views
    bot_session_ids = set(
        PageVisit.objects.filter(
            ~Q(session_id=""),
            id__in=pv_bot_ids if pv_bot_ids else [],
        ).values_list("session_id", flat=True)
    )
    # Also check facility views with obviously bot-like facility_id
    # patterns (though rare, some bots hit random IDs)
    fv_deleted = 0
    if bot_session_ids:
        fv_deleted, _ = FacilityView.objects.filter(
            session_id__in=bot_session_ids
        ).delete()

    # ── SearchQuery ──────────────────────────────────────────────────
    sq_deleted = 0
    if bot_session_ids:
        sq_deleted, _ = SearchQuery.objects.filter(
            session_id__in=bot_session_ids
        ).delete()

    total = pv_deleted + fv_deleted + sq_deleted
    logger.info(
        "Bot cleanup complete: PV=%d  FV=%d  SQ=%d  (total %d)",
        pv_deleted,
        fv_deleted,
        sq_deleted,
        total,
    )
    return {
        "page_visits_deleted": pv_deleted,
        "facility_views_deleted": fv_deleted,
        "search_queries_deleted": sq_deleted,
        "total_deleted": total,
    }
