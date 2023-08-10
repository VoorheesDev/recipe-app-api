from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from recipes.models import Tag
from recipes.serializers import TagSerializer


UserModel = get_user_model()
TAGS_URL = reverse("recipes:tag-list")


def detail_url(tag_id):
    """Create and return a tag detail url."""

    return reverse("recipes:tag-detail", args=[tag_id])


def create_user(email="test@ex.com", password="testpassword"):
    """Create and return a new user."""

    return UserModel.objects.create_user(email=email, password=password)


class PublicTagTest(TestCase):
    """Test anuathenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving tags."""

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagTest(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving list of tags."""

        Tag.objects.create(user=self.user, name="Dessert")
        Tag.objects.create(user=self.user, name="Vegan")

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test list of tags limited to authenticated user."""

        user2 = create_user(email="test2@ex.com", password="test2password")
        Tag.objects.create(user=user2, name="Fruity")
        tag = Tag.objects.create(user=self.user, name="Comfort food")

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)
        self.assertEqual(res.data[0]["id"], tag.id)

    def test_update_tag(self):
        """Test updating a tag is successful."""

        tag = Tag.objects.create(user=self.user, name="After Dinner")

        paylaod = {"name": "Dessert"}
        url = detail_url(tag.id)
        res = self.client.patch(url, paylaod)
        tag.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(tag.name, paylaod["name"])

    def test_delete_tag(self):
        """Test deleting a tag is successful."""

        tag = Tag.objects.create(user=self.user, name="Breakfast")

        url = detail_url(tag.id)
        res = self.client.delete(url)
        tags = Tag.objects.filter(user=self.user)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(tags.exists())
