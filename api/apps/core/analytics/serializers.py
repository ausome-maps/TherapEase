from rest_framework import serializers
from .models import PageVisit, FacilityView, SearchQuery


class PageVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageVisit
        fields = ["id", "path", "referrer", "user_agent", "ip_hash", "session_id", "created_at"]
        read_only_fields = ["id", "created_at"]


class FacilityViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityView
        fields = ["id", "facility_id", "facility_name", "timestamp", "session_id"]
        read_only_fields = ["id", "timestamp"]


class SearchQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchQuery
        fields = ["id", "query_text", "result_count", "filters_applied", "timestamp", "session_id"]
        read_only_fields = ["id", "timestamp"]
