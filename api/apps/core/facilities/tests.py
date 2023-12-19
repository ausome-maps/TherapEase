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
            },
        }
        token, created = Token.objects.get_or_create(user=self.user)
        self.headers = {"Authorization": f"Token {token}"}

    def test_create_facility(self):
        print(self.headers)
        response = self.client.post(
            "/facilities/", self.facility_data, headers=self.headers, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Facilities.objects.count(), 1)
        self.assertEqual(Facilities.objects.get().properties.placename, "Test Facility")

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
        self.assertEqual(Facilities.objects.count(), 0)
