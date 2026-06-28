import logging
import uuid

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_tracking.mixins import LoggingMixin
from django.db.models import Q
from django.conf import settings

from apps.core.facilities.models import Facilities, FacilityProperties
from apps.core.submissions.models import FacilitySubmission
from apps.core.submissions.permissions import SubmissionPermissions
from apps.core.submissions.serializers import (
    FacilitySubmissionAdminSerializer,
    FacilitySubmissionCreateSerializer,
    FacilitySubmissionSerializer,
)
from apps.core.submissions.tasks import (
    task_notify_staff_new_submission,
    task_notify_submitter_approval,
    task_notify_submitter_rejection,
)

logger = logging.getLogger(__name__)


class FacilitySubmissionViewset(LoggingMixin, viewsets.ModelViewSet):
    queryset = FacilitySubmission.objects.all()
    permission_classes = (SubmissionPermissions,)
    authentication_classes = [JWTAuthentication, TokenAuthentication]
    serializer_class = FacilitySubmissionCreateSerializer

    def should_log(self, request, response):
        return response.status_code >= 400

    def get_serializer_class(self):
        if self.action == "create":
            return FacilitySubmissionCreateSerializer
        if self.action in ("update", "partial_update"):
            return FacilitySubmissionAdminSerializer
        return FacilitySubmissionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(
                Q(submitter_email__icontains=search)
                | Q(submitter_name__icontains=search)
                | Q(payload__properties__placename__icontains=search)
            )
        ordering = self.request.query_params.get("ordering", "-created_at")
        if ordering.lstrip("-") in ("created_at", "submitter_email", "submitter_name", "status"):
            qs = qs.order_by(ordering)
        return qs

    def perform_create(self, serializer):
        submission = serializer.save()
        try:
            task_notify_staff_new_submission.delay(submission.id)
        except Exception as e:
            logger.warning(f"Failed to enqueue staff notification for submission {submission.id}: {e}")

    @action(detail=True, methods=["post"])
    def review(self, request, pk=None):
        submission = self.get_object()
        submission.status = "in_review"
        admin_notes = request.data.get("admin_notes", "")
        if admin_notes:
            if submission.admin_notes:
                submission.admin_notes = submission.admin_notes + "\n---\n" + admin_notes
            else:
                submission.admin_notes = admin_notes
        submission.save()
        return Response(FacilitySubmissionSerializer(submission).data)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        submission = self.get_object()

        payload = submission.payload
        props = payload.get("properties", {})
        facility_id = props.get("osm_id", str(uuid.uuid4()))

        facility_properties = FacilityProperties.objects.create(
            osm_id=facility_id,
            info_src_name=props.get("info_src_name", ""),
            info_src_designation=props.get("info_src_designation", ""),
            placename=props.get("placename", ""),
            address=props.get("address", ""),
            region=props.get("region", ""),
            city=props.get("city", ""),
            landmarks_desc=props.get("landmarks_desc", ""),
            contact_number=props.get("contact_number", ""),
            alt_contact_number=props.get("alt_contact_number", ""),
            email_address=props.get("email_address", ""),
            website=props.get("website", ""),
            social_media=props.get("social_media"),
            services_offered=props.get("services_offered") or {},
            other_services=props.get("other_services"),
            caters_to=props.get("caters_to"),
            images=submission.images or [],
            accreditation=props.get("accreditation") or {"paot": 0, "pasp": 0},
            status="active",
        )

        facility = Facilities.objects.get(id=facility_id)
        geometry = payload.get("geometry")
        if isinstance(geometry, dict):
            facility.geometry = geometry
            facility.save()

        submission.status = "merged"
        submission.merged_facility = facility
        admin_notes = request.data.get("admin_notes", "")
        if admin_notes:
            if submission.admin_notes:
                submission.admin_notes = submission.admin_notes + "\n---\n" + admin_notes
            else:
                submission.admin_notes = admin_notes
        submission.save()

        try:
            task_notify_submitter_approval.delay(submission.id)
        except Exception as e:
            logger.warning(f"Failed to enqueue approval notification for submission {submission.id}: {e}")

        return Response(FacilitySubmissionSerializer(submission).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        submission = self.get_object()
        admin_notes = request.data.get("admin_notes", "")
        submission.status = "rejected"
        if admin_notes:
            if submission.admin_notes:
                submission.admin_notes = submission.admin_notes + "\n---\n" + admin_notes
            else:
                submission.admin_notes = admin_notes
        submission.save()

        try:
            task_notify_submitter_rejection.delay(submission.id)
        except Exception as e:
            logger.warning(f"Failed to enqueue rejection notification for submission {submission.id}: {e}")

        return Response(FacilitySubmissionSerializer(submission).data)

    @action(detail=False, methods=["post"], url_path="upload-image")
    def upload_image(self, request):
        from apps.core.submissions.storage import upload_to_minio

        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return Response({"error": "No file provided."}, status=400)

        allowed_extensions = (".jpg", ".jpeg", ".png", ".gif", ".webp")
        if not uploaded_file.name.lower().endswith(allowed_extensions):
            return Response(
                {"error": f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"},
                status=400,
            )

        max_size = 10 * 1024 * 1024  # 10MB
        if uploaded_file.size > max_size:
            return Response({"error": "File too large. Max 10MB."}, status=400)

        result = upload_to_minio(uploaded_file)
        return Response(result)
