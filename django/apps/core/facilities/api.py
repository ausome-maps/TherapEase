from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin
from .permissions import FacilitiesPermissions
from .serializers import Facilities, FacilitiesSerializer

# search
from apps.core.facilities.documents import FacilitiesDocument
from django.db.models import Q


class FacilitiesViewset(LoggingMixin, viewsets.ModelViewSet):
    queryset = Facilities.objects.all()
    permission_classes = (FacilitiesPermissions,)
    serializer_class = FacilitiesSerializer

    def should_log(self, request, response):
        """Log only errors"""
        return response.status_code >= 400

    @action(detail=False, methods=["get", "post"], name="search")
    def search(self, request):
        results = FacilitiesDocument.search().query(
            "term", properties__placename="center"
        )
        res = self.serializer_class(results.to_queryset(), many=True).data
        return Response(res)
