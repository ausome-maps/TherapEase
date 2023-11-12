from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
from rest_framework_tracking.mixins import LoggingMixin
from .models import Profile
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ProfileSerializer,
)


class RegisterView(LoggingMixin, generics.CreateAPIView):
    queryset = User.objects.none()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def should_log(self, request, response):
        """Log only errors"""
        return response.status_code >= 400


class UserViewset(LoggingMixin, viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = UserSerializer

    def should_log(self, request, response):
        """Log only errors"""
        return response.status_code >= 400


class ProfileViewset(LoggingMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def should_log(self, request, response):
        """Log only errors"""
        return response.status_code >= 400

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
