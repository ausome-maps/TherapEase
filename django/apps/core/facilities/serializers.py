from rest_framework import serializers
from .models import Facilities, FacilityProperties


class FacilitiesPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityProperties
        fields = "__all__"


class FacilitiesSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    properties = FacilitiesPropertiesSerializer()

    class Meta:
        model = Facilities
        fields = ["id", "properties", "geometry"]

    def create(self, validated_data):
        property_data = validated_data.pop("properties")
        print(validated_data)
        id = validated_data.pop("id")
        properties = FacilityProperties.objects.create(**property_data)
        facilities = Facilities.objects.create(
            **validated_data, id=id, properties=properties
        )
        return facilities
