from rest_framework import serializers

from objects.models import (
    Building,
    BuildingCoordinates,
)
from .building import BuildingListSerializer


class BuildingCoordinatesSerializer(serializers.ModelSerializer):
    building = serializers.PrimaryKeyRelatedField(
        queryset=Building.objects.all())

    class Meta:
        model = BuildingCoordinates
        fields = (
            "id",
            "lat",
            "lng",
            "building"
        )

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "lat": instance.lat,
            "lng": instance.lng,
            "building": BuildingListSerializer(instance.building).data
        }


class BuildingCoordinatesFullySerializer(serializers.ModelSerializer):
    building = BuildingListSerializer()

    class Meta:
        model = BuildingCoordinates
        fields = (
            "id",
            "lat",
            "lng",
            "building"
        )

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "latitude": instance.lat,
            "longitude": instance.lng,
            "building": BuildingListSerializer(instance.building).data
        }
