from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework_tracking.mixins import LoggingMixin
from django.http import JsonResponse
from django.contrib.postgres.search import SearchVector
from .permissions import FacilitiesPermissions
from .serializers import Facilities, FacilitiesSerializer, FacilityProperties, FacilitiesPropertiesSerializer

SEARCH_RESPONSE_TEMPLATE = {
    "type": "FeatureCollection",
    "name": "Ausome Maps - Therapy Centers",
    "features": [],
}

class FacilitiesPropertiesViewset(LoggingMixin, viewsets.ModelViewSet):
    queryset = FacilityProperties.objects.all()
    permission_classes = (FacilitiesPermissions,)
    serializer_class = FacilitiesPropertiesSerializer

    def should_log(self, request, response):
        """Log only errors"""
        return response.status_code >= 400

class FacilitiesViewset(LoggingMixin, viewsets.ModelViewSet):
    queryset = Facilities.objects.all()
    permission_classes = (FacilitiesPermissions,)
    serializer_class = FacilitiesSerializer

    def should_log(self, request, response):
        """Log only errors"""
        return response.status_code >= 400

    @action(detail=False, methods=["get", "post"], name="search")
    def search(self, request):
        text_search = request.data.get("q", "*")
        start_from = int(request.data.get("from", 0))
        size = int(request.data.get("size", 50))
        if "id:" in text_search:
            text_search = text_search.replace("id:", "")
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
            results = results.filter(search=text_search)
        else:
            results = results.filter()
        SEARCH_RESPONSE_TEMPLATE["total"] = results.count()
        results = results[start_from : start_from + size]
        res = self.serializer_class(results, many=True).data
        SEARCH_RESPONSE_TEMPLATE["features"] = res
        return JsonResponse(SEARCH_RESPONSE_TEMPLATE)
