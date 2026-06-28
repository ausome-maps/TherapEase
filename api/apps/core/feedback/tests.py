from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.facilities.models import Facilities, FacilityProperties
from apps.core.feedback.models import Feedback


class FeedbackTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.api_url = "/feedback/"

        self.properties = FacilityProperties.objects.create(
            osm_id="a" * 32, placename="Test Therapy Center"
        )
        self.facility = Facilities.objects.get(id=self.properties.osm_id)

        self.properties2 = FacilityProperties.objects.create(
            osm_id="b" * 32, placename="Another Center"
        )
        self.facility2 = Facilities.objects.get(id=self.properties2.osm_id)

        self.staff_user = User.objects.create_user(
            username="staff@test.com",
            email="staff@test.com",
            password="staffpass123",
            is_staff=True,
        )
        self.regular_user = User.objects.create_user(
            username="user@test.com",
            email="user@test.com",
            password="userpass123",
        )

        self.valid_payload = {
            "facility": str(self.facility.id),
            "email_address": "test@example.com",
            "contact_number": "+639123456789",
            "data_concerns": "Some data concern here.",
            "usability_concerns": "Some usability concern here.",
        }

    def _get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def _auth_header(self, user):
        return f"Bearer {self._get_token(user)}"

    def test_create_feedback_public(self):
        res = self.client.post(self.api_url, self.valid_payload, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Feedback.objects.count(), 1)
        feedback = Feedback.objects.first()
        self.assertEqual(feedback.email_address, "test@example.com")
        self.assertEqual(feedback.facility, self.facility)
        self.assertEqual(feedback.status, "new")

    def test_create_feedback_missing_required_field_fails(self):
        payload = {
            "facility": str(self.facility.id),
            "email_address": "test@example.com",
            "contact_number": "+639123456789",
            "data_concerns": "Some data concern here.",
        }
        res = self.client.post(self.api_url, payload, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(Feedback.objects.count(), 0)

    def test_create_feedback_invalid_facility_fails(self):
        payload = {
            **self.valid_payload,
            "facility": "00000000-0000-0000-0000-000000000000",
        }
        res = self.client.post(self.api_url, payload, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(Feedback.objects.count(), 0)

    def test_list_feedback_requires_staff(self):
        Feedback.objects.create(
            facility=self.facility,
            email_address="test@example.com",
            contact_number="+639123456789",
            data_concerns="data",
            usability_concerns="usability",
        )
        res = self.client.get(self.api_url)
        self.assertEqual(res.status_code, 401)

        res = self.client.get(
            self.api_url, HTTP_AUTHORIZATION=self._auth_header(self.regular_user)
        )
        self.assertEqual(res.status_code, 403)

        res = self.client.get(
            self.api_url, HTTP_AUTHORIZATION=self._auth_header(self.staff_user)
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 1)

    def test_admin_can_update_status_and_notes(self):
        feedback = Feedback.objects.create(
            facility=self.facility,
            email_address="test@example.com",
            contact_number="+639123456789",
            data_concerns="data",
            usability_concerns="usability",
        )
        res = self.client.patch(
            f"{self.api_url}{feedback.id}",
            {"status": "resolved", "admin_notes": "Reviewed and fixed."},
            format="json",
            HTTP_AUTHORIZATION=self._auth_header(self.staff_user),
        )
        self.assertEqual(res.status_code, 200)
        feedback.refresh_from_db()
        self.assertEqual(feedback.status, "resolved")
        self.assertEqual(feedback.admin_notes, "Reviewed and fixed.")

    def test_admin_cannot_modify_core_fields(self):
        feedback = Feedback.objects.create(
            facility=self.facility,
            email_address="test@example.com",
            contact_number="+639123456789",
            data_concerns="data",
            usability_concerns="usability",
        )
        res = self.client.patch(
            f"{self.api_url}{feedback.id}",
            {
                "email_address": "hacked@evil.com",
                "contact_number": "000",
                "status": "resolved",
            },
            format="json",
            HTTP_AUTHORIZATION=self._auth_header(self.staff_user),
        )
        self.assertEqual(res.status_code, 200)
        feedback.refresh_from_db()
        self.assertEqual(feedback.email_address, "test@example.com")

    def test_filter_by_status(self):
        Feedback.objects.create(
            facility=self.facility,
            email_address="a@test.com",
            contact_number="1",
            data_concerns="d",
            usability_concerns="u",
            status="new",
        )
        Feedback.objects.create(
            facility=self.facility2,
            email_address="b@test.com",
            contact_number="2",
            data_concerns="d",
            usability_concerns="u",
            status="resolved",
        )
        res = self.client.get(
            f"{self.api_url}?status=new",
            HTTP_AUTHORIZATION=self._auth_header(self.staff_user),
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 1)
