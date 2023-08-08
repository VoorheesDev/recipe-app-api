from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from recipes.models import Recipe


UserModel = get_user_model()


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
