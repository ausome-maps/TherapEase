from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.core import mail
from django.contrib.auth.models import Permission
from apps.core.users.models import User, Organization, OrganizationRole, Roles


class UserAppTest(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "hello@example.com",
            "password": "testpassword811",
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
        password = self.user_data["password"]
        u = User.objects.create(**self.user_data)
        u.set_password(password)
        u.save()
        token = Token.objects.get(user__email=self.user_data["username"])
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        # add user to created organization
        self.user = User.objects.get(email=self.user_data["email"])
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.is_active = True
        self.user.save()
        self.organization = Organization.objects.create(
            name="Created Organization", other_metadata={"contact_nos": "0912345678"}
        )
        self.organization.add_member(self.user)
        # create organization role
        self.org_role = OrganizationRole.objects.create(
            organization=self.organization, user=self.user, role=self.role
        )
        # create another user and organization
        self.user_2 = User.objects.create(**self.user_data_2)
        self.client_2 = APIClient()
        token_2 = Token.objects.get(user__email=self.user_data_2["username"])
        self.client_2.credentials(HTTP_AUTHORIZATION=f"Token {token_2}")
        self.organization_2 = Organization.objects.create(
            name="Created Organization 2", other_metadata={"contact_nos": "0912345678"}
        )
        self.organization_2.add_member(self.user_2)
        self.org_role_2 = OrganizationRole.objects.create(
            organization=self.organization_2, user=self.user_2, role=self.role
        )

    def test_user_profile_api(self):
        profile_url = "/users/api/profile/"
        response = self.client.get(profile_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_organization_model_rel(self):
        org_count = Organization.objects.filter().count()
        self.assertEqual(org_count, 2)
        self.assertTrue(self.organization.is_member(self.user))
        # test is_member for non member
        self.assertFalse(self.organization.is_member(self.user_2))
        # test removal of user
        self.organization.remove_member(self.user)
        self.assertFalse(self.organization.is_member(self.user))

    def test_organization_permissions(self):
        updated_org_data = {"name": "updated organization name"}
        org_url = f"/users/organization/{self.organization.id}/"
        response = self.client.put(org_url, format="json", data=updated_org_data)
        self.assertEqual(response.status_code, 200)
        org = Organization.objects.get(id=self.organization.id)
        self.assertEqual(org.name, updated_org_data["name"])

        # the result of this should be 403 since user 2 is not a member of the organization 1
        org_data_2 = {"name": "updated organization name 2"}
        org_url = f"/users/organization/{self.organization.id}/"
        response = self.client_2.put(org_url, format="json", data=org_data_2)
        self.assertEqual(response.status_code, 403)

        # test org creation
        create_org_url = "/users/organization/"
        created_org_data = {
            "name": "created organization name",
            "other_metadata": {"contact_nos": "0912345678"},
        }
        response = self.client.post(
            create_org_url, format="json", data=created_org_data
        )
        org_id = response.json()["data"]["id"]
        self.assertEqual(str(Organization.objects.get(id=org_id).id), org_id)

    def test_simple_jwt_on_protected_api(self):
        token_url = "/auth/jwt/create/"
        credentials = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(token_url, data=credentials, format="json")
        users_url = "/auth/users/"
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.json()['data']['access']}"
        )
        response = self.client.get(users_url, format="json")
        self.assertEqual(response.status_code, 200)


class EmailVerificationTest(APITestCase):
    # endpoints needed
    register_url = "/auth/users/"
    activate_url = "/auth/users/activation/"
    login_url = "/auth/token/login/"
    logout_url = "/auth/token/logout/"
    user_details_url = "/auth/users/"
    # user infofmation
    user_data = {
        "email": "test@example.com",
        "username": "test@example.com",
        "password": "verysecret",
        "password2": "verysecret",
        "first_name": "test",
        "last_name": "user",
    }
    login_data = {"email": "test@example.com", "password": "verysecret"}

    def test_register_with_email_verification(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        # expected response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # expected one email to be send
        self.assertEqual(len(mail.outbox), 1)
        # parse email to get uid and token
        email_lines = mail.outbox[0].body.splitlines()
        activation_link = [line for line in email_lines if "/activate/" in line][0]
        uid, token = activation_link.split("/")[-2:]

        # verify email
        data = {"uid": uid, "token": token}
        response = self.client.post(self.activate_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # login to get the authentication token
        response = self.client.post(self.login_url, self.login_data, format="json")
        self.assertTrue("auth_token" in response.json()["data"]["attributes"])
        token = response.json()["data"]["attributes"]["auth_token"]

        # set token in the header
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        # get user details
        response = self.client.get(self.user_details_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)
        self.assertEqual(
            response.json()["data"][0]["attributes"]["email"], self.user_data["email"]
        )
        self.assertEqual(
            response.json()["data"][0]["attributes"]["username"],
            self.user_data["username"],
        )

        # logout the user
        response = self.client.post(self.logout_url, format="json")
        self.assertEqual(response.status_code, 204)
        response = self.client.get(self.user_details_url, format="json")
        self.assertEqual(response.status_code, 401)
