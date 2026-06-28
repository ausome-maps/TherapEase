from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    facility_name = serializers.CharField(
        source="facility.properties.placename", read_only=True
    )

    class Meta:
        model = Feedback
        fields = [
            "id",
            "facility",
            "facility_name",
            "email_address",
            "contact_number",
            "data_concerns",
            "usability_concerns",
            "status",
            "admin_notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "status", "admin_notes", "created_at", "updated_at"]


class FeedbackAdminSerializer(serializers.ModelSerializer):
    facility_name = serializers.CharField(
        source="facility.properties.placename", read_only=True
    )

    class Meta:
        model = Feedback
        fields = [
            "id",
            "facility",
            "facility_name",
            "email_address",
            "contact_number",
            "data_concerns",
            "usability_concerns",
            "status",
            "admin_notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "facility",
            "facility_name",
            "email_address",
            "contact_number",
            "data_concerns",
            "usability_concerns",
            "created_at",
            "updated_at",
        ]
