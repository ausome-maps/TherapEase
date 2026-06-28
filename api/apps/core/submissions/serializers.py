from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import FacilitySubmission
from apps.core.facilities.api import SERVICE_KEYS

ALLOWED_CATERS_TO = [
    "pediatric",
    "Pediatric",
    "Pediatric Population",
    "adolescent",
    "Adolescent",
    "Adolescent Population",
    "adult",
    "Adult",
    "Adult Population",
]

PH_LNG_MIN = 117
PH_LNG_MAX = 127
PH_LAT_MIN = 4
PH_LAT_MAX = 21


def validate_payload(payload: dict):
    if not isinstance(payload, dict):
        raise ValidationError({"payload": "Must be a JSON object."})

    props = payload.get("properties")
    if not isinstance(props, dict):
        raise ValidationError({"payload.properties": "Required."})

    placename = (props.get("placename") or "").strip()
    if not placename:
        raise ValidationError({"payload.properties.placename": "This field is required."})

    services = props.get("services_offered")
    if isinstance(services, dict):
        for key in services:
            if key not in SERVICE_KEYS:
                raise ValidationError(
                    {f"payload.properties.services_offered.{key}": f"Unknown service key: {key}"}
                )
            svc = services[key]
            if isinstance(svc, dict):
                mode = svc.get("mode", {})
                if isinstance(mode, dict):
                    for m in ["teletherapy", "onsite", "home_service"]:
                        val = mode.get(m)
                        if val is not None and val not in (0, 1, 2, 3):
                            raise ValidationError(
                                {f"payload.properties.services_offered.{key}.mode.{m}": "Must be 0-3."}
                            )

    caters_to = props.get("caters_to")
    if caters_to is not None:
        if not isinstance(caters_to, list):
            raise ValidationError({"payload.properties.caters_to": "Must be a list."})
        for item in caters_to:
            if item not in ALLOWED_CATERS_TO:
                raise ValidationError(
                    {f"payload.properties.caters_to": f"Unknown caters_to value: {item}"}
                )

    accreditation = props.get("accreditation")
    if isinstance(accreditation, dict):
        for key in accreditation:
            if key not in ("paot", "pasp"):
                raise ValidationError(
                    {f"payload.properties.accreditation.{key}": "Only paot and pasp allowed."}
                )
            if accreditation[key] not in (0, 1):
                raise ValidationError(
                    {f"payload.properties.accreditation.{key}": "Must be 0 or 1."}
                )

    geometry = payload.get("geometry")
    if isinstance(geometry, dict):
        geom_type = geometry.get("type")
        coords = geometry.get("coordinates")
        if geom_type != "Point" or not isinstance(coords, list) or len(coords) != 2:
            raise ValidationError({"payload.geometry": "Must be a GeoJSON Point with [lng, lat]."})
        lng, lat = coords[0], coords[1]
        if not isinstance(lng, (int, float)) or not isinstance(lat, (int, float)):
            raise ValidationError({"payload.geometry": "Coordinates must be numbers."})
        if not (PH_LNG_MIN <= lng <= PH_LNG_MAX):
            raise ValidationError(
                {"payload.geometry.coordinates": f"Longitude must be between {PH_LNG_MIN} and {PH_LNG_MAX}."}
            )
        if not (PH_LAT_MIN <= lat <= PH_LAT_MAX):
            raise ValidationError(
                {"payload.geometry.coordinates": f"Latitude must be between {PH_LAT_MIN} and {PH_LAT_MAX}."}
            )

    email = (props.get("email_address") or "").strip()
    if email:
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValidationError({"payload.properties.email_address": "Enter a valid email address."})


class FacilitySubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilitySubmission
        fields = [
            "id",
            "payload",
            "images",
            "status",
            "admin_notes",
            "submitted_by",
            "submitter_email",
            "submitter_name",
            "merged_facility",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "admin_notes",
            "submitted_by",
            "merged_facility",
            "created_at",
            "updated_at",
        ]

    def validate_payload(self, value):
        validate_payload(value)
        return value

    def validate_submitter_email(self, value):
        if not value:
            raise ValidationError("This field is required.")
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["submitted_by"] = request.user
        return super().create(validated_data)


class FacilitySubmissionAdminSerializer(serializers.ModelSerializer):
    placename = serializers.SerializerMethodField(read_only=True)
    submitter_email = serializers.CharField(read_only=True)

    class Meta:
        model = FacilitySubmission
        fields = [
            "id",
            "payload",
            "images",
            "status",
            "admin_notes",
            "submitted_by",
            "submitter_email",
            "submitter_name",
            "merged_facility",
            "created_at",
            "updated_at",
            "placename",
        ]
        read_only_fields = [
            "id",
            "payload",
            "images",
            "submitted_by",
            "submitter_name",
            "merged_facility",
            "created_at",
            "updated_at",
            "placename",
        ]

    def get_placename(self, obj):
        try:
            return obj.payload.get("properties", {}).get("placename", "")
        except (AttributeError, KeyError):
            return ""


class FacilitySubmissionSerializer(serializers.ModelSerializer):
    placename = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FacilitySubmission
        fields = [
            "id",
            "payload",
            "images",
            "status",
            "admin_notes",
            "submitted_by",
            "submitter_email",
            "submitter_name",
            "merged_facility",
            "created_at",
            "updated_at",
            "placename",
        ]
        read_only_fields = [
            "id",
            "status",
            "admin_notes",
            "submitted_by",
            "merged_facility",
            "created_at",
            "updated_at",
            "placename",
        ]

    def get_placename(self, obj):
        try:
            return obj.payload.get("properties", {}).get("placename", "")
        except (AttributeError, KeyError):
            return ""
