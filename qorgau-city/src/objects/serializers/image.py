from rest_framework import serializers

from objects.models import (
    BuildingImage,
    SubBuildingImage,
)


class BuildingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingImage
        fields = ['id', 'image', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class SubBuildingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubBuildingImage
        fields = ['id', 'image', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class MultipleBuildingImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )

    def create(self, validated_data):
        building = validated_data['building']
        image_list = validated_data.pop('images')
        image_objects = []
        for image in image_list:
            image_objects.append(BuildingImage.objects.create(building=building, image=image))
        return image_objects


class MultipleSubBuildingImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )

    def create(self, validated_data):
        subbuilding = validated_data['subbuilding']
        image_list = validated_data.pop('images')
        image_objects = []
        for image in image_list:
            image_objects.append(SubBuildingImage.objects.create(subbuilding=subbuilding, image=image))
        return image_objects
