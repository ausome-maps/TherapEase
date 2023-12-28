from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework_tracking.mixins import LoggingMixin
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.postgres.search import SearchVector
from .permissions import FacilitiesPermissions
from .serializers import (
    Facilities,
    FacilitiesSerializer,
    FacilityProperties,
    FacilitiesPropertiesSerializer,
)

SEARCH_RESPONSE_TEMPLATE = {
    "type": "FeatureCollection",
    "name": "Ausome Maps - Therapy Centers",
    "features": [],
    "total": 0,
}


class FacilitiesPropertiesViewset(LoggingMixin, viewsets.ModelViewSet):
    queryset = FacilityProperties.objects.exclude(status="inactive")
    permission_classes = (FacilitiesPermissions,)
    serializer_class = FacilitiesPropertiesSerializer

    def should_log(self, request, response):
        """Log only errors"""
        return response.status_code >= 400


class FacilitiesViewset(LoggingMixin, viewsets.ModelViewSet):
    queryset = Facilities.objects.exclude(properties__status="inactive")
    permission_classes = (FacilitiesPermissions,)
    serializer_class = FacilitiesSerializer

    def should_log(self, request, response):
        """Log only errors"""
        return response.status_code >= 400

    def _build_services_offered_query(self, services_offered):
        query = Q()
        for service in services_offered:
            query |= Q(properties__services_offered__contains=service)
        return query

    def _send_a_not_yet_implemented_filter(self):
        SEARCH_RESPONSE_TEMPLATE[
            "message"
        ] = "One of your filters is not yet implemented."
        return JsonResponse(SEARCH_RESPONSE_TEMPLATE)

    @action(detail=False, methods=["get", "post"], name="search")
    def search(self, request):
        text_search = request.data.get("q", "*")
        start_from = int(request.data.get("from", 0))
        size = int(request.data.get("size", 50))
        extra_filters = request.data.get("filters", [])

        if "id:" in text_search:
            text_search = text_search.replace("id:", "")

        # TODO: Optimize the query build up the various queries
        property_filter = Q()
        for extra_filter in extra_filters:
            if extra_filter == "services_offered":
                property_filter &= self._build_services_offered_query(
                    extra_filters[extra_filter]
                )
            else:
                return self._send_a_not_yet_implemented_filter()

        results = Facilities.objects.annotate(
            search=SearchVector(
                "properties__osm_id",
                "properties__placename",
                "properties__address",
                "properties__region",
                "properties__city",
            )
        )
        if text_search != "*":
            results = results.filter(search=text_search).exclude(
                properties__status="inactive"
            )
        else:
            results = results.exclude(properties__status="inactive")
        if len(property_filter.children) != 0:
            results = results.filter(property_filter)
        SEARCH_RESPONSE_TEMPLATE["total"] = results.count()
        results = results[start_from : start_from + size]
        res = self.serializer_class(results, many=True).data
        SEARCH_RESPONSE_TEMPLATE["features"] = res
        return JsonResponse(SEARCH_RESPONSE_TEMPLATE)
