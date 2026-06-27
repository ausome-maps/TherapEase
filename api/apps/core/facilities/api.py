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
from apps.core.users.models import OrganizationRole

SEARCH_RESPONSE_TEMPLATE = {
    "type": "FeatureCollection",
    "name": "Ausome Maps - Therapy Centers",
    "features": [],
    "total": 0,
}

SERVICE_KEYS = [
    "speechlanguagetherapy",
    "speechlanguagepathology",
    "occupationaltherapy",
    "behavioraltherapy",
    "physicaltherapy",
    "lifeskillstraining",
    "socialskillstraining",
    "integration",
    "integrationprogram",
    "jobcoaching",
    "specialeducation",
    "spedtutorials",
    "parentcoaching",
    "educationsessionforfamilies",
    "feeding",
    "counseling",
    "psychotherapy",
    "abatherapy",
    "mnri",
    "sensoryintegration",
    "playschool",
    "dysphagiamanagement",
    "orthoses",
    "homeschoolfacilitation",
    "rehabconsultation",
]


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

    def perform_create(self, serializer):
        facility = serializer.save()
        self._assign_to_organization(facility)

    def _assign_to_organization(self, facility):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return
        user_org_roles = OrganizationRole.objects.filter(
            user=user, status="active"
        ).select_related("organization")
        for org_role in user_org_roles:
            org_role.organization.add_facility(facility)

    def _build_services_offered_query(self, services_offered):
        query = Q()
        delivery_modes = ["teletherapy", "onsite", "home_service"]
        for service in services_offered:
            svc_query = Q()
            for dm in delivery_modes:
                svc_query |= Q(
                    **{f"properties__services_offered__{service}__mode__{dm}__gt": 0}
                )
            query |= svc_query
        return query

    def _build_accreditation_query(self, accreditation):
        query = Q()
        for key, value in accreditation.items():
            if value:
                query &= Q(**{f"properties__accreditation__{key}": 1})
        return query

    def _build_mode_query(self, modes):
        query = Q()
        for mode in modes:
            for svc_key in SERVICE_KEYS:
                query |= Q(
                    **{f"properties__services_offered__{svc_key}__mode__{mode}__gt": 0}
                )
        return query

    def _build_session_type_query(self, session_types):
        query = Q()
        delivery_modes = ["teletherapy", "onsite", "home_service"]
        for st in session_types:
            lookup_vals = [1, 3] if st == "individual" else [2, 3]
            for svc_key in SERVICE_KEYS:
                for dm in delivery_modes:
                    query |= Q(
                        **{
                            f"properties__services_offered__{svc_key}__mode__{dm}__in": lookup_vals
                        }
                    )
        return query

    def _build_caters_to_query(self, caters_to):
        query = Q()
        for target in caters_to:
            query |= Q(properties__caters_to__contains=[target])
        return query

    @action(detail=False, methods=["get", "post"], name="search")
    def search(self, request):
        text_search = request.data.get("q", "*")
        start_from = int(request.data.get("from", 0))
        size = int(request.data.get("size", 50))
        extra_filters = request.data.get("filters", {})

        if "id:" in text_search:
            text_search = text_search.replace("id:", "")

        property_filter = Q()
        for filter_key, filter_value in extra_filters.items():
            if filter_key == "services_offered" and filter_value:
                property_filter &= self._build_services_offered_query(filter_value)
            elif filter_key == "accreditation" and filter_value:
                property_filter &= self._build_accreditation_query(filter_value)
            elif filter_key == "mode" and filter_value:
                property_filter &= self._build_mode_query(filter_value)
            elif filter_key == "session_type" and filter_value:
                property_filter &= self._build_session_type_query(filter_value)
            elif filter_key == "caters_to" and filter_value:
                property_filter &= self._build_caters_to_query(filter_value)

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
