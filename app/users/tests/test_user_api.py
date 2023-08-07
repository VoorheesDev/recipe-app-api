from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


UserModel = get_user_model()
CREATE_USER_URL = reverse("users:create")
TOKEN_URL = reverse("users:token")
ME_URL = reverse("users:me")


def create_user(**params):
    """Create and return a new user."""

    return UserModel.objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the public features of user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""

        payload = {
            "email": "test@ex.com",
            "password": "testpassword",
            "name": "Test Name",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = UserModel.objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_create_user_with_email_exists_error(self):
        """Test an error returned if user with such email exists."""

        payload = {
            "email": "test@ex.com",
            "password": "testpassword",
            "name": "Test Name",
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error returned if password is less than 5 chars."""

        payload = {
            "email": "test@ex.com",
            "password": "pass",
            "name": "Test Name",
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = UserModel.objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test token is generated for valid credentials."""

        user_details = {
            "email": "test@ex.com",
            "password": "testpassword",
            "name": "Test Name",
        }
        create_user(**user_details)

        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test return error for invalid credentials."""

        user_details = {
            "email": "test@ex.com",
            "password": "testpassword",
            "name": "Test Name",
        }
        create_user(**user_details)

        payload = {"email": user_details["email"], "password": "badpassword"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""

        payload = {"email": "test@ex.com", "password": ""}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            email="test@ex.com",
            password="testpassword",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"email": self.user.email, "name": self.user.name})

    def test_post_me_not_allowed(self):
        """Test POST method is not allowed for `me` endpoint."""

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test update the user profile for the authenticated user."""

        payload = {"name": "New name", "password": "newpassword"}

        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
