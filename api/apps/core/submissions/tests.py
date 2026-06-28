import uuid
from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from apps.core.facilities.models import Facilities, FacilityProperties
from apps.core.submissions.models import FacilitySubmission


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class FacilitySubmissionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.api_url = "/submissions/"

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

        self.valid_props = {
            "placename": "New Therapy Center",
            "address": "123 Mabini St, Quezon City",
            "region": "NCR – National Capital Region",
            "city": "Quezon City",
            "landmarks_desc": "Near the mall",
            "contact_number": "+639123456789",
            "alt_contact_number": "02-1234-5678",
            "email_address": "center@example.com",
            "website": "https://example.com",
            "social_media": {"facebook": "fb.com/center", "instagram": "@center"},
            "info_src_name": "Juan Dela Cruz",
            "info_src_designation": "Owner",
            "services_offered": {
                "occupationaltherapy": {
                    "label": "Occupational Therapy",
                    "mode": {"teletherapy": 1, "onsite": 0, "home_service": 0},
                },
                "specialeducation": {
                    "label": "Special Education",
                    "mode": {"teletherapy": 2, "onsite": 1, "home_service": 0},
                },
            },
            "caters_to": ["Pediatric", "Adolescent"],
            "accreditation": {"paot": 1, "pasp": 0},
            "images": [],
        }

        self.valid_payload = {
            "payload": {
                "properties": self.valid_props,
                "geometry": {"type": "Point", "coordinates": [121.05, 14.67]},
            },
            "submitter_email": "submitter@example.com",
            "submitter_name": "Maria Santos",
        }

    def _get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def _auth_header(self, user):
        return f"Bearer {self._get_token(user)}"

    def test_create_submission_public(self):
        res = self.client.post(self.api_url, self.valid_payload, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(FacilitySubmission.objects.count(), 1)
        submission = FacilitySubmission.objects.first()
        self.assertEqual(submission.submitter_email, "submitter@example.com")
        self.assertEqual(submission.status, "new")
        self.assertIsNone(submission.submitted_by)
        self.assertIn("properties", submission.payload)
        self.assertEqual(
            submission.payload["properties"]["placename"], "New Therapy Center"
        )

    def test_create_submission_auth_user_sets_submitted_by(self):
        payload = {
            "payload": self.valid_payload["payload"],
        }
        res = self.client.post(
            self.api_url,
            payload,
            format="json",
            HTTP_AUTHORIZATION=self._auth_header(self.regular_user),
        )
        self.assertEqual(res.status_code, 400)

        payload["submitter_email"] = "authuser@example.com"
        res = self.client.post(
            self.api_url,
            payload,
            format="json",
            HTTP_AUTHORIZATION=self._auth_header(self.regular_user),
        )
        self.assertEqual(res.status_code, 201)
        submission = FacilitySubmission.objects.first()
        self.assertEqual(submission.submitted_by, self.regular_user)

    def test_create_submission_missing_placename_fails(self):
        payload = {
            "payload": {
                "properties": self.valid_props | {"placename": ""},
                "geometry": {"type": "Point", "coordinates": [121.05, 14.67]},
            },
            "submitter_email": "submitter@example.com",
        }
        res = self.client.post(self.api_url, payload, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(FacilitySubmission.objects.count(), 0)

    def test_create_submission_missing_payload_fails(self):
        res = self.client.post(
            self.api_url, {"submitter_email": "test@example.com"}, format="json"
        )
        self.assertEqual(res.status_code, 400)
        self.assertEqual(FacilitySubmission.objects.count(), 0)

    def test_create_submission_missing_submitter_email_fails(self):
        payload = {"payload": self.valid_payload["payload"]}
        res = self.client.post(self.api_url, payload, format="json")
        self.assertEqual(res.status_code, 400)

    def test_create_submission_invalid_service_key_fails(self):
        bad_props = self.valid_props.copy()
        bad_props["services_offered"] = {
            "invalid_key": {
                "label": "Bad Service",
                "mode": {"teletherapy": 1, "onsite": 0, "home_service": 0},
            }
        }
        payload = {
            "payload": {
                "properties": bad_props,
                "geometry": {"type": "Point", "coordinates": [121.05, 14.67]},
            },
            "submitter_email": "test@example.com",
        }
        res = self.client.post(self.api_url, payload, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(FacilitySubmission.objects.count(), 0)

    def test_create_submission_coordinates_outside_ph_fails(self):
        for coords, desc in [
            ([100, 14], "lng too low"),
            ([130, 14], "lng too high"),
            ([121, 1], "lat too low"),
            ([121, 25], "lat too high"),
        ]:
            payload = {
                "payload": {
                    "properties": self.valid_props,
                    "geometry": {"type": "Point", "coordinates": coords},
                },
                "submitter_email": "test@example.com",
            }
            res = self.client.post(self.api_url, payload, format="json")
            self.assertEqual(res.status_code, 400, f"Should fail for {desc}")
            self.assertEqual(FacilitySubmission.objects.count(), 0)

    def test_create_submission_valid_email_succeeds(self):
        payload = {
            "payload": {
                "properties": self.valid_props,
                "geometry": {"type": "Point", "coordinates": [121.05, 14.67]},
            },
            "submitter_email": "valid@example.com",
        }
        res = self.client.post(self.api_url, payload, format="json")
        self.assertEqual(res.status_code, 201)

    def test_create_submission_invalid_accreditation_key_fails(self):
        bad_props = self.valid_props.copy()
        bad_props["accreditation"] = {"paot": 1, "pasp": 0, "fake": 1}
        payload = {
            "payload": {
                "properties": bad_props,
                "geometry": {"type": "Point", "coordinates": [121.05, 14.67]},
            },
            "submitter_email": "test@example.com",
        }
        res = self.client.post(self.api_url, payload, format="json")
        self.assertEqual(res.status_code, 400)

    def test_list_submissions_requires_staff(self):
        FacilitySubmission.objects.create(
            payload=self.valid_payload["payload"],
            submitter_email="test@example.com",
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

    def test_admin_can_review(self):
        submission = FacilitySubmission.objects.create(
            payload=self.valid_payload["payload"],
            submitter_email="test@example.com",
        )
        url = f"{self.api_url}{submission.id}/review"
        res = self.client.post(
            url,
            {"admin_notes": "Looking into this."},
            format="json",
            HTTP_AUTHORIZATION=self._auth_header(self.staff_user),
        )
        self.assertEqual(res.status_code, 200)
        submission.refresh_from_db()
        self.assertEqual(submission.status, "in_review")
        self.assertEqual(submission.admin_notes, "Looking into this.")

    def test_regular_user_cannot_review(self):
        submission = FacilitySubmission.objects.create(
            payload=self.valid_payload["payload"],
            submitter_email="test@example.com",
        )
        res = self.client.post(
            f"{self.api_url}{submission.id}/review",
            HTTP_AUTHORIZATION=self._auth_header(self.regular_user),
        )
        self.assertEqual(res.status_code, 403)

    def test_admin_can_reject(self):
        submission = FacilitySubmission.objects.create(
            payload=self.valid_payload["payload"],
            submitter_email="test@example.com",
        )
        res = self.client.post(
            f"{self.api_url}{submission.id}/reject",
            {"admin_notes": "Duplicate entry."},
            format="json",
            HTTP_AUTHORIZATION=self._auth_header(self.staff_user),
        )
        self.assertEqual(res.status_code, 200)
        submission.refresh_from_db()
        self.assertEqual(submission.status, "rejected")
        self.assertEqual(submission.admin_notes, "Duplicate entry.")

    def test_admin_can_approve_merges_facility(self):
        submission = FacilitySubmission.objects.create(
            payload=self.valid_payload["payload"],
            submitter_email="test@example.com",
        )
        res = self.client.post(
            f"{self.api_url}{submission.id}/approve",
            {"admin_notes": "Looks good."},
            format="json",
            HTTP_AUTHORIZATION=self._auth_header(self.staff_user),
        )
        self.assertEqual(res.status_code, 200)
        submission.refresh_from_db()
        self.assertEqual(submission.status, "merged")
        self.assertIn("Looks good.", submission.admin_notes)
        self.assertIsNotNone(submission.merged_facility)

        facility = submission.merged_facility
        self.assertEqual(
            facility.properties.placename, "New Therapy Center"
        )
        self.assertEqual(facility.properties.address, "123 Mabini St, Quezon City")
        self.assertEqual(facility.properties.region, "NCR – National Capital Region")
        self.assertEqual(facility.properties.city, "Quezon City")
        self.assertEqual(facility.properties.status, "active")
        self.assertEqual(facility.geometry["coordinates"], [121.05, 14.67])
        self.assertIn("occupationaltherapy", facility.properties.services_offered)
        self.assertEqual(
            facility.properties.services_offered["occupationaltherapy"]["mode"][
                "teletherapy"
            ],
            1,
        )
        self.assertEqual(facility.properties.caters_to, ["Pediatric", "Adolescent"])
        self.assertEqual(facility.properties.accreditation, {"paot": 1, "pasp": 0})

    def test_approved_facility_visible_in_search(self):
        submission = FacilitySubmission.objects.create(
            payload=self.valid_payload["payload"],
            submitter_email="test@example.com",
        )
        self.client.post(
            f"{self.api_url}{submission.id}/approve",
            format="json",
            HTTP_AUTHORIZATION=self._auth_header(self.staff_user),
        )
        res = self.client.get(
            "/facilities/search",
            {"q": "New Therapy Center"},
            format="json",
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data["features"]), 1)
        self.assertEqual(
            data["features"][0]["properties"]["placename"], "New Therapy Center"
        )

    def test_admin_cannot_modify_core_fields(self):
        submission = FacilitySubmission.objects.create(
            payload=self.valid_payload["payload"],
            submitter_email="test@example.com",
        )
        new_payload = {
            "payload": {
                "properties": {"placename": "Hacked Name"},
                "geometry": {"type": "Point", "coordinates": [0, 0]},
            },
            "submitter_email": "hacked@evil.com",
            "status": "in_review",
        }
        res = self.client.patch(
            f"{self.api_url}{submission.id}",
            new_payload,
            format="json",
            HTTP_AUTHORIZATION=self._auth_header(self.staff_user),
        )
        self.assertEqual(res.status_code, 200)
        submission.refresh_from_db()
        self.assertEqual(submission.submitter_email, "test@example.com")
        self.assertEqual(
            submission.payload["properties"]["placename"], "New Therapy Center"
        )

    def test_admin_can_update_status_and_notes(self):
        submission = FacilitySubmission.objects.create(
            payload=self.valid_payload["payload"],
            submitter_email="test@example.com",
        )
        res = self.client.patch(
            f"{self.api_url}{submission.id}",
            {"status": "in_review", "admin_notes": "Review started."},
            format="json",
            HTTP_AUTHORIZATION=self._auth_header(self.staff_user),
        )
        self.assertEqual(res.status_code, 200)
        submission.refresh_from_db()
        self.assertEqual(submission.status, "in_review")
        self.assertEqual(submission.admin_notes, "Review started.")

    def test_filter_by_status(self):
        FacilitySubmission.objects.create(
            payload=self.valid_payload["payload"],
            submitter_email="a@test.com",
            status="new",
        )
        p2 = self.valid_payload["payload"].copy()
        p2["properties"] = self.valid_props | {"placename": "Another Center"}
        FacilitySubmission.objects.create(
            payload=p2, submitter_email="b@test.com", status="rejected"
        )
        res = self.client.get(
            f"{self.api_url}?status=new",
            HTTP_AUTHORIZATION=self._auth_header(self.staff_user),
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data["results"]), 1)

    def test_pending_submission_not_in_facilities_list(self):
        FacilitySubmission.objects.create(
            payload=self.valid_payload["payload"],
            submitter_email="test@example.com",
        )
        res = self.client.get(
            "/facilities/search",
            {"q": "New Therapy Center"},
            format="json",
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["total"], 0)

    def test_create_submission_invalid_geom_type_fails(self):
        payload = {
            "payload": {
                "properties": self.valid_props,
                "geometry": {"type": "Polygon", "coordinates": []},
            },
            "submitter_email": "test@example.com",
        }
        res = self.client.post(self.api_url, payload, format="json")
        self.assertEqual(res.status_code, 400)

    def test_create_submission_bad_coords_not_numbers_fails(self):
        payload = {
            "payload": {
                "properties": self.valid_props,
                "geometry": {"type": "Point", "coordinates": ["abc", "def"]},
            },
            "submitter_email": "test@example.com",
        }
        res = self.client.post(self.api_url, payload, format="json")
        self.assertEqual(res.status_code, 400)

    def test_create_submission_invalid_service_mode_value_fails(self):
        bad_props = self.valid_props.copy()
        bad_props["services_offered"] = {
            "occupationaltherapy": {
                "label": "Occupational Therapy",
                "mode": {"teletherapy": 5, "onsite": 0, "home_service": 0},
            }
        }
        payload = {
            "payload": {
                "properties": bad_props,
                "geometry": {"type": "Point", "coordinates": [121.05, 14.67]},
            },
            "submitter_email": "test@example.com",
        }
        res = self.client.post(self.api_url, payload, format="json")
        self.assertEqual(res.status_code, 400)

    def test_upload_image_no_file_returns_error(self):
        res = self.client.post(f"{self.api_url}upload-image")
        self.assertEqual(res.status_code, 400)
        self.assertIn("error", res.data)
