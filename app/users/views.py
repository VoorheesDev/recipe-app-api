from rest_framework import authentication, generics, permissions
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


class ManageUserAPIView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""

        return self.request.user
