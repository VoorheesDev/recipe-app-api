from django.contrib.auth import get_user_model
from django.test import TestCase


UserModel = get_user_model()


class UserTest(TestCase):
    """Test user model."""

    def test_create_user_with_email_successful(self):
        """Ensure creating a user with an email is successful."""

        user = UserModel.objects.create_user(email="test@example.com", password="testpassword")

        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpassword"))

    def test_create_user_without_email_raises_error(self):
        """Ensure creating a user without an email raises an error."""

        with self.assertRaises(TypeError):
            UserModel.objects.create_user()
        with self.assertRaises(ValueError):
            UserModel.objects.create_user(email="")
        with self.assertRaises(ValueError):
            UserModel.objects.create_user(email="", password="testpassword")

    def test_create_superuser_with_email_successful(self):
        """Ensure creating a superuser with an email is successful."""

        superuser = UserModel.objects.create_superuser(
            email="test@example.com", password="testpassword"
        )

        self.assertEqual(superuser.email, "test@example.com")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_without_email_raises_error(self):
        """Ensure creating a superuser without an email raises an error."""

        with self.assertRaises(TypeError):
            UserModel.objects.create_superuser()
        with self.assertRaises(ValueError):
            UserModel.objects.create_superuser(email="")
        with self.assertRaises(ValueError):
            UserModel.objects.create_superuser(email="", password="testpassword")

    def test_create_superuser_with_wrong_permissions_raises_error(self):
        """Ensure creating a superuser with wrong permissions raises an error."""

        with self.assertRaises(ValueError):
            UserModel.objects.create_superuser(
                email="test@example.com", password="testpassword", is_staff=False
            )
        with self.assertRaises(ValueError):
            UserModel.objects.create_superuser(
                email="test@example.com", password="testpassword", is_superuser=False
            )
