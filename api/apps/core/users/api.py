from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
from rest_framework_tracking.mixins import LoggingMixin
from .models import Profile, Organization
from .serializers import (
    RegisterSerializer,
    ProfileSerializer,
    OrganizationSerializer,
)
from .permissions import OrganizationPermissions


class RegisterView(LoggingMixin, generics.CreateAPIView):
    queryset = User.objects.none()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

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


class OrganizationViewset(LoggingMixin, viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    permission_classes = (OrganizationPermissions,)
    serializer_class = OrganizationSerializer
