from rest_framework import permissions, viewsets
from rest_framework_tracking.mixins import LoggingMixin
from .models import Profile, Organization
from .serializers import (
    ProfileSerializer,
    OrganizationSerializer,
)
from .permissions import OrganizationPermissions


class ProfileViewset(LoggingMixin, viewsets.ModelViewSet):
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
