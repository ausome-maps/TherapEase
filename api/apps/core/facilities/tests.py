import uuid
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Facilities, FacilityProperties


class FacilitiesTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.facility_data = {
            "geometry": {"type": "Point", "coordinates": [121.545819, 16.682762]},
            "properties": {
                "placename": "Test Facility",
                "address": "123 Test Street",
                "city": "Test City",
                "region": "Test Region",
                "services_offered": {
                    "mnri": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "MNRI",
                    },
                    "feeding": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "Feeding",
                    },
                    "orthoses": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "Orthoses (Splinting)",
                    },
                    "abatherapy": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "ABA Therapy",
                    },
                    "counseling": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "Counseling",
                    },
                    "playschool": {
                        "mode": {"onsite": 2, "teletherapy": 0, "home_service": 0},
                        "label": "Play School",
                    },
                    "integration": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "Integration",
                    },
                    "jobcoaching": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "Job Coaching",
                    },
                    "psychotherapy": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "Psychotherapy",
                    },
                    "spedtutorials": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "SpEd Tutorials",
                    },
                    "parentcoaching": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "Parent Coaching",
                    },
                    "physicaltherapy": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "Physical Therapy",
                    },
                    "specialeducation": {
                        "mode": {"onsite": 0, "teletherapy": 1, "home_service": 1},
                        "label": "Special Education",
                    },
                    "behavioraltherapy": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "Behavioral Therapy",
                    },
                    "rehabconsultation": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "Rehab Consultation",
                    },
                    "integrationprogram": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "Integration Program",
                    },
                    "lifeskillstraining": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "Life Skills Training",
                    },
                    "sensoryintegration": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "Sensory Integration",
                    },
                    "dysphagiamanagement": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "Dysphagia Management",
                    },
                    "occupationaltherapy": {
                        "mode": {"onsite": 1, "teletherapy": 1, "home_service": 0},
                        "label": "Occupational Therapy",
                    },
                    "socialskillstraining": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "Social Skills Training",
                    },
                    "speechlanguagetherapy": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "Speech-Language Therapy",
                    },
                    "homeschoolfacilitation": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "Homeschool Facilitation",
                    },
                    "speechlanguagepathology": {
                        "mode": {"onsite": 1, "teletherapy": 1, "home_service": 0},
                        "label": "Speech-Language Pathology",
                    },
                    "educationsessionforfamilies": {
                        "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0},
                        "label": "Education Session for Families",
                    },
                },
            },
        }
        token, _ = Token.objects.get_or_create(user=self.user)
        self.headers = {"Authorization": f"Token {token}"}
        self.client.post(
            "/facilities/", self.facility_data, headers=self.headers, format="json"
        )

    def test_create_facility(self):
        self.facility_data["properties"]["placename"] = "New Facility"
        response = self.client.post(
            "/facilities/", self.facility_data, headers=self.headers, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Facilities.objects.count(), 2)
        self.assertEqual(
            Facilities.objects.get(
                properties__placename="New Facility"
            ).properties.placename,
            "New Facility",
        )

    def test_update_facility(self):
        fp_id = str(uuid.uuid4())
        _ = FacilityProperties.objects.create(
            osm_id=fp_id,
            placename="Original Facility",
            address="123 Original Street",
            region="Original region",
        )
        facility = Facilities.objects.get(id=fp_id)
        updated_data = {
            "properties": {
                "placename": "Updated Facility",
                "address": "456 Updated Street",
            }
        }
        response = self.client.put(
            f"/facilities/{facility.id}",
            updated_data,
            format="json",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        facility.refresh_from_db()
        self.assertEqual(facility.properties.placename, "Updated Facility")
        self.assertEqual(facility.properties.address, "456 Updated Street")
        self.assertEqual(facility.properties.region, "Original region")

    def test_delete_facility(self):
        fp_id = str(uuid.uuid4())
        _ = FacilityProperties.objects.create(
            osm_id=fp_id,
            placename="Original Facility",
            address="123 Original Street",
            region="Original region",
        )
        facility = Facilities.objects.get(id=fp_id)
        response = self.client.delete(
            f"/facilities/{facility.id}", headers=self.headers
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Facilities.objects.count(), 1)

    def test_search_facility(self):
        search_with_hit = {"q": "Test Facility"}
        response = self.client.post(
            "/facilities/search", data=search_with_hit, format="json"
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json()["features"]))
        extra_filters_with_hit = {
            "filters": {
                "services_offered": [
                    {
                        "orthoses": {
                            "mode": {"onsite": 0, "teletherapy": 0, "home_service": 0}
                        }
                    }
                ]
            }
        }
        response = self.client.post(
            "/facilities/search", data=extra_filters_with_hit, format="json"
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.json()["features"]))
        extra_filters_without_hit = {
            "filters": {
                "services_offered": [
                    {
                        "orthoses": {
                            "mode": {"onsite": 1, "teletherapy": 0, "home_service": 0}
                        }
                    }
                ]
            }
        }
        response = self.client.post(
            "/facilities/search", data=extra_filters_without_hit, format="json"
        )
        self.assertEqual(0, len(response.json()["features"]))
        extra_filters_not_implemented = {"filters": {"caters_to": ["pediatric"]}}
        response = self.client.post(
            "/facilities/search", data=extra_filters_not_implemented, format="json"
        )
        self.assertEqual(0, len(response.json()["features"]))
        self.assertEqual(
            "One of your filters is not yet implemented.", response.json()["message"]
        )
