import json
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework_tracking.mixins import LoggingMixin
from django.http import JsonResponse
from django.contrib.postgres.search import SearchVector
from .permissions import FacilitiesPermissions
from .serializers import Facilities, FacilitiesSerializer

# search
# from apps.core.facilities.documents import FacilitiesDocument


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
        text_search = request.data.get("q", "*")
        start_from = int(request.data.get("start_from", 0))
        size = int(request.data.get("size", 50))
        # q = {
        #     "query_string": {
        #         "query": text_search,
        #         "fields": [
        #             "properties.osm_id",
        #             "properties.placename",
        #             "properties.address",
        #             "properties.city",
        #             "properties.region",
        #         ],
        #     }
        # }
        # results = FacilitiesDocument.search().query(q)[start_from:size]
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
        results = results[start_from: start_from+size]
        # res = self.serializer_class(results.to_queryset(), many=True).data
        res = self.serializer_class(results, many=True).data
        template["features"] = res
        # template["total"] = results.execute().hits.total.to_dict()
        template["total"] = results.count()
        return JsonResponse(template)
