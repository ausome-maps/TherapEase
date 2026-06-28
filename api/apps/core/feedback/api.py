from rest_framework import viewsets
from rest_framework_tracking.mixins import LoggingMixin

from .models import Feedback
from .serializers import FeedbackSerializer, FeedbackAdminSerializer
from .permissions import FeedbackPermissions


class FeedbackViewset(LoggingMixin, viewsets.ModelViewSet):
    queryset = Feedback.objects.all().select_related("facility__properties")
    permission_classes = (FeedbackPermissions,)

    def should_log(self, request, response):
        return response.status_code >= 400

    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            return FeedbackAdminSerializer
        return FeedbackSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        facility = self.request.query_params.get("facility")
        if facility:
            qs = qs.filter(facility_id=facility)
        return qs
