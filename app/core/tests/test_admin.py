from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


UserModel = get_user_model()


class AdminSiteTest(TestCase):
    """Tests for django admin."""

    def setUp(self):
        """Create user and client."""

        self.client = Client()
        self.admin_user = UserModel.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword",
        )
        self.client.force_login(self.admin_user)

        self.user = UserModel.objects.create_user(
            email="test@example.com", password="testpassword", name="Test User"
        )

    def test_users_list(self):
        """Test users are listed on page."""

        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test user edit page works."""

        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test user create page works."""

        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
