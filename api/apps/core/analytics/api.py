import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import PageVisit, FacilityView, SearchQuery
from .permissions import AnalyticsPermissions
from .serializers import (
    PageVisitSerializer,
    FacilityViewSerializer,
    SearchQuerySerializer,
)
from .utils import is_bot_request

logger = logging.getLogger(__name__)


class AnalyticsViewset(viewsets.GenericViewSet):
    permission_classes = (AnalyticsPermissions,)

    @action(detail=False, methods=["post"], url_path="page-visit")
    def track_page_visit(self, request):
        """Track a page visit (bot traffic is silently dropped)."""
        if is_bot_request(request):
            return Response({"status": "ignored", "reason": "bot"}, status=status.HTTP_200_OK)
        serializer = PageVisitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "ok"}, status=201)

    @action(detail=False, methods=["post"], url_path="facility-view")
    def track_facility_view(self, request):
        """Track a facility detail page view (bot traffic is silently dropped)."""
        if is_bot_request(request):
            return Response({"status": "ignored", "reason": "bot"}, status=status.HTTP_200_OK)
        serializer = FacilityViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "ok"}, status=201)

    @action(detail=False, methods=["post"], url_path="search-query")
    def track_search_query(self, request):
        """Track a search query (bot traffic is silently dropped)."""
        if is_bot_request(request):
            return Response({"status": "ignored", "reason": "bot"}, status=status.HTTP_200_OK)
        serializer = SearchQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "ok"}, status=201)

    # ── Admin / cleanup actions ────────────────────────────────────────

    @action(
        detail=False,
        methods=["post"],
        url_path="cleanup-bots",
        permission_classes=[AnalyticsPermissions],
    )
    def cleanup_bots(self, request):
        """Remove all analytics entries that match known bot patterns.

        Only accessible to staff/superusers.
        """
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({"error": "Permission denied"}, status=403)

        from .tasks import cleanup_bot_analytics

        result = cleanup_bot_analytics.delay()
        return Response({
            "status": "queued",
            "task_id": result.id,
        })


class PageVisitViewset(viewsets.ReadOnlyModelViewSet):
    queryset = PageVisit.objects.all()
    permission_classes = (AnalyticsPermissions,)
    serializer_class = PageVisitSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        days = self.request.query_params.get("days")
        if days:
            from datetime import timedelta
            from django.utils import timezone

            cutoff = timezone.now() - timedelta(days=int(days))
            qs = qs.filter(created_at__gte=cutoff)
        return qs


class FacilityViewViewset(viewsets.ReadOnlyModelViewSet):
    queryset = FacilityView.objects.all()
    permission_classes = (AnalyticsPermissions,)
    serializer_class = FacilityViewSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        days = self.request.query_params.get("days")
        if days:
            from datetime import timedelta
            from django.utils import timezone

            cutoff = timezone.now() - timedelta(days=int(days))
            qs = qs.filter(timestamp__gte=cutoff)
        return qs


class SearchQueryViewset(viewsets.ReadOnlyModelViewSet):
    queryset = SearchQuery.objects.all()
    permission_classes = (AnalyticsPermissions,)
    serializer_class = SearchQuerySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        days = self.request.query_params.get("days")
        if days:
            from datetime import timedelta
            from django.utils import timezone

            cutoff = timezone.now() - timedelta(days=int(days))
            qs = qs.filter(timestamp__gte=cutoff)
        return qs
