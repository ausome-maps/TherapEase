from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework_tracking.mixins import LoggingMixin
from django.http import JsonResponse
from .permissions import FacilitiesPermissions
from .serializers import Facilities, FacilitiesSerializer

# search
from apps.core.facilities.documents import FacilitiesDocument


template = {
    "type": "FeatureCollection",
    "name": "Ausome Maps - Therapy Centers",
    "features": [],
}


class FacilitiesViewset(LoggingMixin, viewsets.ModelViewSet):
    queryset = Facilities.objects.all()
    permission_classes = (FacilitiesPermissions,)
    serializer_class = FacilitiesSerializer

    def should_log(self, request, response):
        """Log only errors"""
        return response.status_code >= 400

    @action(detail=False, methods=["get", "post"], name="search")
    def search(self, request):
        text_search = request.query_params.get("q", "*")
        start_from = int(request.query_params.get("start_from", 0))
        size = int(request.query_params.get("size", 50))
        q = {
            "multi_match": {
                "query": text_search,
                "fields": [
                    "properties.placename",
                    "properties.address",
                    "properties.city",
                    "properties.region",
                ],
            }
        }
        results = FacilitiesDocument.search().query(q)[start_from:size]
        res = self.serializer_class(results.to_queryset(), many=True).data
        template["features"] = res
        return JsonResponse(template)
