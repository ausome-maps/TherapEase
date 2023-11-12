from datetime import datetime, timedelta, timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from apps.core.users.models import User, Profile
from apps.core.users.serializers import RegisterSerializer
from .tasks import send_registration_email


# Create your tests here.
class UserAppTest(APITestCase):
    def setUp(self):
        self.data = {
            "username": "hello@example.com",
            "password": "testpassword811",
            "password2": "testpassword811",
            "email": "hello@example.com",
            "first_name": "example first name",
            "last_name": "example last name",
            "organization": "example organization",
        }
        self.register_serializer = RegisterSerializer(data=self.data)
        self.register_serializer.is_valid()
        self.register_serializer.save()
        token = Token.objects.get(user__email=self.data["username"])
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    def test_user_register_serializer(self):
        u = User.objects.filter().count()
        p = Profile.objects.filter().count()
        t = Token.objects.filter().count()
        # check if other entries are created by signals.py
        self.assertEqual(u, p)
        self.assertEqual(u, t)

    def test_user_profile_api(self):
        profile_url = "/users/api/profile/"
        response = self.client.get(profile_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email_function(self):
        email = send_registration_email(
            self.data["first_name"], datetime.now(), self.data["email"]
        )
        self.assertEqual(email, self.data["email"])
