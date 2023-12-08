import uuid
from rest_framework import serializers
from .models import Facilities, FacilityProperties


class FacilitiesPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityProperties
        fields = "__all__"


class FacilitiesSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    properties = FacilitiesPropertiesSerializer()

    class Meta:
        model = Facilities
        fields = ["id", "properties", "geometry"]

    def create(self, validated_data):
        property_data = validated_data.pop("properties")
        id = validated_data.pop("id", str(uuid.uuid4()))
        properties = FacilityProperties.objects.create(osm_id=id, **property_data)
        facilities = Facilities.objects.create(
            **validated_data, id=id, properties=properties
        )
        return facilities

    def update(self, instance, validated_data):
        property_data = validated_data.pop("properties")
        id = validated_data.pop("id", str(instance.id))
        _ = FacilityProperties.objects.filter(osm_id=id).update(**property_data)
        Facilities.objects.filter(id=id).update(**validated_data)
        return Facilities.objects.get(id=id)
