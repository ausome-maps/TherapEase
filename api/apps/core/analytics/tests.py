"""
Tests for the analytics app: bot detection, tracking endpoints,
staff-only read access, day filtering, cleanup-bots, and models.
"""
import uuid
from datetime import timedelta

from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PageVisit, FacilityView, SearchQuery, ReportRecipient
from .utils import is_bot, is_bot_request


# ---------------------------------------------------------------------------
# Bot detection utility tests
# ---------------------------------------------------------------------------

class BotDetectionTests(TestCase):
    """Unit tests for is_bot() and is_bot_request()."""

    def test_empty_ua_is_bot(self):
        self.assertTrue(is_bot(""))
        self.assertTrue(is_bot(None))
        self.assertTrue(is_bot("   "))

    def test_short_ua_is_bot(self):
        self.assertTrue(is_bot("curl"))

    def test_known_bot_patterns(self):
        bots = [
            "Googlebot/2.1",
            "Mozilla/5.0 (compatible; bingbot/2.0)",
            "DuckDuckBot/1.0",
            "Baiduspider",
            "YandexBot",
            "AhrefsBot",
            "SemrushBot",
            "python-requests/2.28",
            "curl/7.68.0",
            "HeadlessChrome",
            "PhantomJS",
            "UptimeRobot/2.0",
            "Pingdom.com_bot",
            "Bytespider",
        ]
        for ua in bots:
            self.assertTrue(is_bot(ua), f"Should detect as bot: {ua}")

    def test_real_browsers_are_not_bots(self):
        humans = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/120.0",
        ]
        for ua in humans:
            self.assertFalse(is_bot(ua), f"Should NOT be bot: {ua}")

    def test_case_insensitive_matching(self):
        self.assertTrue(is_bot("bOt/1.0"))
        self.assertTrue(is_bot("GOOGLEBOT"))
        self.assertTrue(is_bot("SpIdEr"))

    def test_is_bot_request_integration(self):
        """Test is_bot_request via actual API endpoint (bot detection in tracking)."""
        # Already covered by AnalyticsTrackingEndpointTests:
        # - Bot user_agent in payload → ignored
        # - Bot HTTP_USER_AGENT header → ignored
        # - Real browser UA → tracked successfully
        # This test serves as a documentation placeholder for the integration path.
        pass


# ---------------------------------------------------------------------------
# Analytics tracking endpoints
# ---------------------------------------------------------------------------

class AnalyticsTrackingEndpointTests(TestCase):
    """Tests for POST endpoints that receive analytics events."""

    def setUp(self):
        self.client = APIClient()
        self.track_page_visit_url = "/analytics/track/page-visit"
        self.track_facility_view_url = "/analytics/track/facility-view"
        self.track_search_query_url = "/analytics/track/search-query"
        self.browser_ua = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        )
        # Set a realistic User-Agent on the test client to avoid bot detection
        self.client._default_headers = {
            "HTTP_USER_AGENT": self.browser_ua,
        }

    def test_track_page_visit_success(self):
        res = self.client.post(
            self.track_page_visit_url,
            {
                "path": "/search",
                "referrer": "https://google.com",
                "user_agent": self.browser_ua,
                "session_id": "abc-123",
            },
            format="json",
            HTTP_USER_AGENT=self.browser_ua,
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(PageVisit.objects.count(), 1)
        pv = PageVisit.objects.first()
        self.assertEqual(pv.path, "/search")
        self.assertEqual(pv.referrer, "https://google.com")

    def test_track_facility_view_success(self):
        res = self.client.post(
            self.track_facility_view_url,
            {
                "facility_id": str(uuid.uuid4()),
                "facility_name": "Test Center",
                "user_agent": self.browser_ua,
                "session_id": "abc-123",
            },
            format="json",
            HTTP_USER_AGENT=self.browser_ua,
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(FacilityView.objects.count(), 1)

    def test_track_search_query_success(self):
        res = self.client.post(
            self.track_search_query_url,
            {
                "query_text": "speech therapy",
                "result_count": 5,
                "filters_applied": {"mode": ["teletherapy"]},
                "user_agent": self.browser_ua,
                "session_id": "abc-123",
            },
            format="json",
            HTTP_USER_AGENT=self.browser_ua,
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(SearchQuery.objects.count(), 1)
        sq = SearchQuery.objects.first()
        self.assertEqual(sq.query_text, "speech therapy")
        self.assertEqual(sq.result_count, 5)

    def test_bot_traffic_is_silently_ignored(self):
        """Bot tracking requests return 200 but create no records."""
        res = self.client.post(
            self.track_page_visit_url,
            {
                "path": "/",
                "user_agent": "Googlebot/2.1",
            },
            format="json",
            HTTP_USER_AGENT="Googlebot/2.1",
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "ignored")
        self.assertEqual(PageVisit.objects.count(), 0)

    def test_bot_traffic_from_http_header_ignored(self):
        """Bot traffic detected via HTTP header is also silently dropped."""
        res = self.client.post(
            self.track_page_visit_url,
            {"path": "/", "user_agent": self.browser_ua},
            format="json",
            HTTP_USER_AGENT="Bingbot/2.0",
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "ignored")
        self.assertEqual(PageVisit.objects.count(), 0)

    def test_track_page_visit_minimal_payload(self):
        """Path-only tracking should work."""
        res = self.client.post(
            self.track_page_visit_url,
            {"path": "/", "user_agent": self.browser_ua},
            format="json",
            HTTP_USER_AGENT=self.browser_ua,
        )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(PageVisit.objects.count(), 1)


# ---------------------------------------------------------------------------
# Staff-only read access
# ---------------------------------------------------------------------------

class AnalyticsReadAccessTests(TestCase):
    """Tests that analytics data is only readable by staff/superusers."""

    def setUp(self):
        self.client = APIClient()
        self.page_visits_url = "/analytics/page-visits"
        self.facility_views_url = "/analytics/facility-views"
        self.search_queries_url = "/analytics/search-queries"

        self.browser_ua = "Mozilla/5.0 Chrome/120.0.0.0"

        # Create some test data
        PageVisit.objects.create(
            path="/", referrer="", user_agent=self.browser_ua, session_id="s1"
        )
        FacilityView.objects.create(
            facility_id=str(uuid.uuid4()), facility_name="Center A", session_id="s1"
        )
        SearchQuery.objects.create(
            query_text="test", result_count=3, session_id="s1"
        )

        self.staff = User.objects.create_user(
            username="staff@test.com",
            email="staff@test.com",
            password="staffpass123",
            is_staff=True,
        )
        self.regular = User.objects.create_user(
            username="user@test.com",
            email="user@test.com",
            password="userpass123",
        )

    def _auth_header(self, user):
        refresh = RefreshToken.for_user(user)
        return f"Bearer {str(refresh.access_token)}"

    def test_unauthenticated_cannot_read(self):
        for url in [self.page_visits_url, self.facility_views_url, self.search_queries_url]:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 401, f"Should be 401 for {url}")

    def test_regular_user_cannot_read(self):
        token = self._auth_header(self.regular)
        for url in [self.page_visits_url, self.facility_views_url, self.search_queries_url]:
            res = self.client.get(url, HTTP_AUTHORIZATION=token)
            self.assertEqual(res.status_code, 403, f"Should be 403 for {url}")

    def test_staff_can_read_page_visits(self):
        res = self.client.get(
            self.page_visits_url,
            HTTP_AUTHORIZATION=self._auth_header(self.staff),
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn("results", res.data)

    def test_staff_can_read_facility_views(self):
        res = self.client.get(
            self.facility_views_url,
            HTTP_AUTHORIZATION=self._auth_header(self.staff),
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn("results", res.data)

    def test_staff_can_read_search_queries(self):
        res = self.client.get(
            self.search_queries_url,
            HTTP_AUTHORIZATION=self._auth_header(self.staff),
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn("results", res.data)

    def test_superuser_can_read(self):
        self.staff.is_superuser = True
        self.staff.is_staff = False
        self.staff.save()
        res = self.client.get(
            self.page_visits_url,
            HTTP_AUTHORIZATION=self._auth_header(self.staff),
        )
        self.assertEqual(res.status_code, 200)

    def test_days_filter_on_page_visits(self):
        """Filter by days should only return recent records."""
        old = PageVisit.objects.create(
            path="/old",
            user_agent=self.browser_ua,
            session_id="old",
        )
        old.created_at = timezone.now() - timedelta(days=10)
        old.save()

        res = self.client.get(
            f"{self.page_visits_url}?days=7",
            HTTP_AUTHORIZATION=self._auth_header(self.staff),
        )
        self.assertEqual(res.status_code, 200)
        # The old record (10 days ago) should be excluded
        old_ids = [r["id"] for r in res.data["results"]]
        self.assertNotIn(str(old.id), old_ids)

    def test_days_filter_on_facility_views(self):
        old = FacilityView.objects.create(
            facility_id=str(uuid.uuid4()),
            session_id="old",
        )
        old.timestamp = timezone.now() - timedelta(days=10)
        old.save()

        res = self.client.get(
            f"{self.facility_views_url}?days=7",
            HTTP_AUTHORIZATION=self._auth_header(self.staff),
        )
        self.assertEqual(res.status_code, 200)
        old_ids = [r["id"] for r in res.data["results"]]
        self.assertNotIn(str(old.id), old_ids)

    def test_days_filter_on_search_queries(self):
        old = SearchQuery.objects.create(
            query_text="old",
            result_count=0,
            session_id="old",
        )
        old.timestamp = timezone.now() - timedelta(days=10)
        old.save()

        res = self.client.get(
            f"{self.search_queries_url}?days=7",
            HTTP_AUTHORIZATION=self._auth_header(self.staff),
        )
        self.assertEqual(res.status_code, 200)
        old_ids = [r["id"] for r in res.data["results"]]
        self.assertNotIn(str(old.id), old_ids)


# ---------------------------------------------------------------------------
# Cleanup-bots endpoint
# ---------------------------------------------------------------------------

@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class CleanupBotsEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cleanup_url = "/analytics/cleanup-bots"

        self.staff = User.objects.create_user(
            username="staff@test.com",
            email="staff@test.com",
            password="staffpass123",
            is_staff=True,
        )
        self.regular = User.objects.create_user(
            username="user@test.com",
            email="user@test.com",
            password="userpass123",
        )

    def _auth_header(self, user):
        refresh = RefreshToken.for_user(user)
        return f"Bearer {str(refresh.access_token)}"

    def test_cleanup_unauthenticated_denied(self):
        res = self.client.post(self.cleanup_url)
        self.assertEqual(res.status_code, 403)

    def test_cleanup_regular_user_denied(self):
        res = self.client.post(
            self.cleanup_url,
            HTTP_AUTHORIZATION=self._auth_header(self.regular),
        )
        self.assertEqual(res.status_code, 403)

    def test_cleanup_by_staff_queues_task(self):
        res = self.client.post(
            self.cleanup_url,
            HTTP_AUTHORIZATION=self._auth_header(self.staff),
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "queued")
        self.assertIn("task_id", data)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class AnalyticsModelTests(TestCase):
    def test_page_visit_str(self):
        pv = PageVisit.objects.create(path="/search")
        pv.refresh_from_db()
        self.assertIn("/search", str(pv))

    def test_facility_view_str(self):
        fid = str(uuid.uuid4())
        fv = FacilityView.objects.create(facility_id=fid)
        fv.refresh_from_db()
        self.assertIn(fid, str(fv))

    def test_search_query_str(self):
        sq = SearchQuery.objects.create(query_text="therapy", result_count=3)
        sq.refresh_from_db()
        self.assertIn("therapy", str(sq))

    def test_page_visit_ordering(self):
        pv1 = PageVisit.objects.create(path="/a")
        pv2 = PageVisit.objects.create(path="/b")
        results = list(PageVisit.objects.all())
        # Should be ordered by -created_at, so newest first
        self.assertEqual(results[0].id, pv2.id)

    def test_facility_view_indexes(self):
        # Verify indexes exist (no error on create)
        fid = str(uuid.uuid4())
        fv = FacilityView.objects.create(facility_id=fid, facility_name="Test")
        self.assertIsNotNone(fv.id)

    def test_search_query_filters_json_default(self):
        sq = SearchQuery.objects.create(query_text="test", result_count=0)
        sq.refresh_from_db()
        self.assertEqual(sq.filters_applied, {})

    def test_report_recipient_str(self):
        rr = ReportRecipient.objects.create(email="test@example.com", enabled=True)
        self.assertIn("✓", str(rr))
        self.assertIn("test@example.com", str(rr))

        rr.enabled = False
        rr.save()
        self.assertIn("✗", str(rr))
