from rest_framework import generics

from users.serializers import UserSerializer


class CreateUserAPIView(generics.CreateAPIView):
    """Create a new user in a system."""

    serializer_class = UserSerializer
