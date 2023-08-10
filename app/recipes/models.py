from django.conf import settings
from django.db import models


class Recipe(models.Model):
    """Model to represent a recipe."""

    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField("Tag")

    def __str__(self):
        """Return readable representation of the model."""

        return self.title


class Tag(models.Model):
    """Model to represent a tag for filtering recipes."""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        """Return readable representation of the model."""

        return self.name
