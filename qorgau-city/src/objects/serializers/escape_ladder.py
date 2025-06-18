from rest_framework import serializers

from objects.models import EscapeLadderImage


class EscapeLadderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscapeLadderImage
        fields = ('id', 'image', 'uploaded_at')


class MultipleEscapeLadderImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True
    )

    def create(self, validated_data):
        building = validated_data['building']
        image_objects = []

        for image in validated_data['images']:
            image_object = EscapeLadderImage.objects.create(
                building=building,
                image=image
            )
            image_objects.append(image_object)

        return image_objects