from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from users.serializers import AuthTokenSerializer, UserSerializer


class CreateUserAPIView(generics.CreateAPIView):
    """Create a new user in a system."""

    serializer_class = UserSerializer


class CreateTokenAPIView(ObtainAuthToken):
    """Create a new token for user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES  # to enable it in browsable API
