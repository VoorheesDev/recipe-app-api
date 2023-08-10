from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from recipes.models import Recipe, Tag


UserModel = get_user_model()


def create_user(email="test@ex.com", password="testpassword"):
    """Create and return a new user."""

    return UserModel.objects.create_user(email=email, password=password)


class RecipeTest(TestCase):
    """Test recipe model."""

    def test_create_recipe(self):
        """Test creating a recipe is successful."""

        user = UserModel.objects.create_user(
            email="test@ex.com",
            password="testpassword",
        )
        recipe = Recipe.objects.create(
            user=user,
            title="Test recipe title",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Test recipe description",
        )

        self.assertEqual(str(recipe), recipe.title)


class TagTest(TestCase):
    """Test tag model."""

    def test_create_tag(self):
        """Test creating a tag is successful."""

        user = create_user()
        tag = Tag.objects.create(user=user, name="Tag1")

        self.assertEqual(str(tag), tag.name)
