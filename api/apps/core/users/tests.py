from datetime import datetime
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Permission
from apps.core.users.models import User, Profile, Organization, OrganizationRole, Roles
from apps.core.users.serializers import RegisterSerializer
from .tasks import send_registration_email


# Create your tests here.
class UserAppTest(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "hello@example.com",
            "password": "testpassword811",
            "password2": "testpassword811",
            "email": "hello@example.com",
            "first_name": "example first name",
            "last_name": "example last name",
        }

        self.user_data_2 = {
            "username": "hello1@example.com",
            "password": "testpassword8111",
            "email": "hello1@example.com",
            "first_name": "example first name2",
            "last_name": "example last name2",
        }
        # configure org permissions
        perm = Permission.objects.get(codename="manage_organization")
        self.role = Roles.objects.create(
            name="admin",
            role_type="org",
        )
        self.role.permissions.add(perm)
        # create user 
        self.register_serializer = RegisterSerializer(data=self.user_data)
        self.register_serializer.is_valid()
        self.register_serializer.save()
        token = Token.objects.get(user__email=self.user_data["username"])
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        # add user to created organization
        self.user = User.objects.get(email=self.user_data["email"])
        self.organization = Organization.objects.create(
            name="Created Organization",
            other_metadata={"contact_nos": "0912345678"}
        )
        self.organization.add_member(self.user)
        # create organization role
        self.org_role = OrganizationRole.objects.create(
            organization=self.organization,
            user=self.user,
            role=self.role
        )
        # create another user but don't assign to org
        self.user_2 = User.objects.create(**self.user_data_2)

    def test_user_register_serializer(self):
        u = User.objects.filter().count()
        p = Profile.objects.filter().count()
        t = Token.objects.filter().count()
        # check if other entries are created by signals.py
        self.assertEqual(u, p)
        self.assertEqual(u, t)
        # # test email function
        # self.skipTest("skipping test_email")
        # email = send_registration_email(
        #     self.user_data["first_name"], datetime.now(), self.user_data["email"]
        # )
        # self.assertEqual(email, self.user_data["email"])

    def test_user_profile_api(self):
        profile_url = "/users/api/profile/"
        response = self.client.get(profile_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_organization_model_rel(self):
        org_count = Organization.objects.filter().count()
        self.assertEqual(org_count, 1)
        self.assertTrue(self.organization.is_member(self.user))
        # test is_member for non member
        self.assertFalse(self.organization.is_member(self.user_2))
        # test removal of user
        self.organization.remove_member(self.user)
        self.assertFalse(self.organization.is_member(self.user))

    def test_organization_permissions(self):
        org_data = {"name": "updated organization name"}
        org_url = f"/users/organization/{self.organization.id}/"
        response = self.client.put(org_url, format="json", data=org_data)
        self.assertEqual(response.status_code, 200)
        org = Organization.objects.all()[0]
        self.assertEqual(org.name, org_data["name"])
        pass