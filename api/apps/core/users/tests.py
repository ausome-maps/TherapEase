from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.core import mail
from django.test import override_settings
from django.contrib.auth.models import Permission
from apps.core.users.models import User, Organization, OrganizationRole, Roles, Profile


class UserAppTest(APITestCase):
    user_data = {
        "username": "hello@example.com",
        "password": "testpassword811",
        "email": "hello@example.com",
        "first_name": "example first name",
        "last_name": "example last name",
    }

    user_data_2 = {
        "username": "hello1@example.com",
        "password": "testpassword8111",
        "email": "hello1@example.com",
        "first_name": "example first name2",
        "last_name": "example last name2",
    }

    def setUp(self):
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
        profile = Profile.objects.get(user=self.user)
        profile_url = f"/users/profile/{str(profile.id)}/"
        response = self.client.get(profile_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_profile = {
            "user": {"first_name": "updated first name"},
            "other_metadata": {"contact_nos": "01234567"},
        }
        response = self.client.patch(profile_url, format="json", data=updated_profile)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        user = data.get("user", data)
        self.assertEqual(updated_profile["user"]["first_name"], user["first_name"])
        self.assertEqual(
            updated_profile["other_metadata"]["contact_nos"],
            data["other_metadata"]["contact_nos"],
        )

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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        org_id = response.json().get("id")
        self.assertIsNotNone(org_id)
        self.assertEqual(str(Organization.objects.get(id=org_id).id), org_id)

    def test_simple_jwt_on_protected_api(self):
        token_url = "/auth/jwt/create/"
        credentials = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(token_url, data=credentials, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token_data = response.json()
        access_token = token_data.get("access")
        self.assertIsNotNone(access_token, f"No access token in response: {token_data}")
        users_url = "/auth/users/"
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(users_url, format="json")
        self.assertEqual(response.status_code, 200)


class EmailVerificationTest(APITestCase):
    # endpoints needed
    register_url = "/auth/users/"
    activate_url = "/auth/users/activation/"
    login_url = "/auth/token/login/"
    logout_url = "/auth/token/logout/"
    user_details_url = "/auth/users/me/"
    # user infofmation
    user_data = {
        "email": "test@example.com",
        "username": "test@example.com",
        "password": "verysecret",
        "re_password": "verysecret",
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        login_data = response.json()
        token = login_data.get(
            "auth_token",
            login_data.get("data", {}).get("attributes", {}).get("auth_token"),
        )
        self.assertIsNotNone(token, f"No auth_token in response: {login_data}")

        # set token in the header
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        # get user details
        response = self.client.get(self.user_details_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        # /auth/users/me/ returns a single user object
        user_data = response_json.get("data", response_json)
        user_attrs = user_data.get("attributes", user_data)
        self.assertEqual(
            user_attrs.get("email", user_attrs.get("username")), self.user_data["email"]
        )

        # logout the user
        response = self.client.post(self.logout_url, format="json")
        self.assertEqual(response.status_code, 204)
        response = self.client.get(self.user_details_url, format="json")
        self.assertEqual(response.status_code, 401)

    def test_register_with_email_and_password_only(self):
        """Frontend registers with only email + password and password confirmation."""
        payload = {
            "email": "frontend@example.com",
            "password": "frontendpass123",
            "re_password": "frontendpass123",
        }
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=payload["email"])
        self.assertTrue(user.username)
        self.assertEqual(len(mail.outbox), 1)

    def test_register_weak_password_returns_field_error(self):
        """Weak password should return a field-level error the frontend can display."""
        payload = {
            "email": "weakpass@example.com",
            "password": "password",
            "re_password": "password",
        }
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        # JSON:API renderer returns a list of error objects.
        errors = (
            data
            if isinstance(data, list)
            else data.get("errors", []) if isinstance(data, dict) else []
        )
        self.assertTrue(
            any("password" in e.get("source", {}).get("pointer", "") for e in errors)
            or any("password" in str(e.get("detail", "")).lower() for e in errors)
        )


class AuthFeatureFlagTest(APITestCase):
    register_url = "/auth/users/"
    login_url = "/auth/jwt/create/"
    refresh_url = "/auth/jwt/refresh/"

    def test_register_blocked_when_disabled(self):
        with override_settings(FEATURE_AUTH_ENABLED=0):
            response = self.client.post(
                self.register_url,
                {"email": "disabled@example.com", "password": "testpass123"},
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertIn("disabled", response.json()["detail"])

    def test_login_blocked_when_disabled(self):
        with override_settings(FEATURE_AUTH_ENABLED=0):
            response = self.client.post(
                self.login_url,
                {"email": "disabled@example.com", "password": "testpass123"},
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_register_succeeds_when_enabled(self):
        with override_settings(FEATURE_AUTH_ENABLED=1):
            response = self.client.post(
                self.register_url,
                {"email": "enabled@example.com", "password": "testpass123", "re_password": "testpass123"},
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_facility_search_still_works_when_disabled(self):
        with override_settings(FEATURE_AUTH_ENABLED=0):
            response = self.client.post(
                "/facilities/search",
                {"filters": {}},
                format="json",
            )
            self.assertIn(response.status_code, [200, 400])


class AdminStatsTest(APITestCase):
    staff_data = {
        "username": "staff@example.com",
        "password": "staffpass123",
        "email": "staff@example.com",
    }
    user_data = {
        "username": "regular@example.com",
        "password": "regularpass123",
        "email": "regular@example.com",
    }

    def setUp(self):
        self.staff = User.objects.create(**self.staff_data)
        self.staff.set_password(self.staff_data["password"])
        self.staff.is_staff = True
        self.staff.is_active = True
        self.staff.save()

        self.regular = User.objects.create(**self.user_data)
        self.regular.set_password(self.user_data["password"])
        self.regular.is_active = True
        self.regular.save()

        self.stats_url = "/users/admin/stats/"

    def _get_jwt(self, email, password):
        response = self.client.post(
            "/auth/jwt/create/",
            {"email": email, "password": password},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.json()["access"]

    def test_staff_can_access_stats(self):
        token = self._get_jwt(self.staff_data["email"], self.staff_data["password"])
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.stats_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("users", data)
        self.assertIn("organizations", data)
        self.assertIsInstance(data["users"]["total"], int)

    def test_superuser_can_access_stats(self):
        self.staff.is_superuser = True
        self.staff.is_staff = False
        self.staff.save()
        token = self._get_jwt(self.staff_data["email"], self.staff_data["password"])
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.stats_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_staff_denied(self):
        token = self._get_jwt(self.user_data["email"], self.user_data["password"])
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.stats_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_denied(self):
        response = self.client.get(self.stats_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
