from rest_framework import serializers
from objects.models import SubBuilding
from specifications.models import (
    ExternalWallMaterialChoice, InnerWallMaterialChoice,
    RoofChoice, StairsMaterialChoice, StairsTypeChoice,
    LightingTypeChoice, VentilationTypeChoice, HeatingChoice,
    SecurityChoice, StairsClassificationChoice
)
from .image import SubBuildingImageSerializer


class ExternalWallMaterialChoiceSerializer(serializers.ListSerializer):
    child = serializers.CharField()


class InnerWallMaterialChoiceSerializer(serializers.ListSerializer):
    child = serializers.CharField()


class RoofChoiceSerializer(serializers.ListSerializer):
    child = serializers.CharField()


class StairsMaterialChoiceSerializer(serializers.ListSerializer):
    child = serializers.CharField()


class StairsTypeChoiceSerializer(serializers.ListSerializer):
    child = serializers.CharField()


class StairsClassificationChoiceSerializer(serializers.ListSerializer):
    child = serializers.CharField()


class LightingTypeChoiceSerializer(serializers.ListSerializer):
    child = serializers.CharField()


class VentilationTypeChoiceSerializer(serializers.ListSerializer):
    child = serializers.CharField()


class HeatingChoiceSerializer(serializers.ListSerializer):
    child = serializers.CharField()


class SecurityChoiceSerializer(serializers.ListSerializer):
    child = serializers.CharField()


class SubBuildingSerializer(serializers.ModelSerializer):
    images = SubBuildingImageSerializer(many=True, read_only=True)
    external_walls_material = ExternalWallMaterialChoiceSerializer()
    inner_walls_material = InnerWallMaterialChoiceSerializer()
    roof = RoofChoiceSerializer()
    stairs_material = StairsMaterialChoiceSerializer()
    stairs_type = StairsTypeChoiceSerializer()
    stairs_classification = StairsClassificationChoiceSerializer()
    lighting = LightingTypeChoiceSerializer()
    ventilation = VentilationTypeChoiceSerializer()
    heating = HeatingChoiceSerializer()
    security = SecurityChoiceSerializer()

    class Meta:
        model = SubBuilding
        fields = (
            'id', 'subbuilding_type', 'subbuilding_subtype', 'subbuilding_optional_subtype_type', 'subbuilding_characteristics',
            'title', 'functional_purpose', 'date_commissioning',
            'fire_resistance_rating', 'structural_po_class',
            'functional_po_class', 'rating', 'change_functional_purpose_date',
            'floor_number', 'total_floors', 'building_foundation',
            'external_walls_material', 'inner_walls_material', 'roof',
            'stairs_material', 'stairs_type', 'stairs_classification',
            'building_height', 'area', 'volume', 'lighting',
            'emergency_lighting', 'ventilation', 'heating', 'security',
            'year_construction_reconstruction', 'images',
        )

    def _get_or_create_choices(self, model_class, names):
        objects = []
        for name in names:
            obj, _ = model_class.objects.get_or_create(name=name)
            objects.append(obj)
        return objects

    def create(self, validated_data):
        # Extract all many-to-many fields
        external_walls_data = validated_data.pop('external_walls_material', [])
        inner_walls_data = validated_data.pop('inner_walls_material', [])
        roof_data = validated_data.pop('roof', [])
        stairs_material_data = validated_data.pop('stairs_material', [])
        stairs_type_data = validated_data.pop('stairs_type', [])
        stairs_classification_data = validated_data.pop('stairs_classification', [])
        lighting_data = validated_data.pop('lighting', [])
        ventilation_data = validated_data.pop('ventilation', [])
        heating_data = validated_data.pop('heating', [])
        security_data = validated_data.pop('security', [])

        # Create the SubBuilding instance
        instance = SubBuilding.objects.create(**validated_data)

        # Handle each many-to-many relationship
        if external_walls_data:
            instance.external_walls_material.set(
                self._get_or_create_choices(ExternalWallMaterialChoice, external_walls_data)
            )
        if inner_walls_data:
            instance.inner_walls_material.set(
                self._get_or_create_choices(InnerWallMaterialChoice, inner_walls_data)
            )
        if roof_data:
            instance.roof.set(
                self._get_or_create_choices(RoofChoice, roof_data)
            )
        if stairs_material_data:
            instance.stairs_material.set(
                self._get_or_create_choices(StairsMaterialChoice, stairs_material_data)
            )
        if stairs_type_data:
            instance.stairs_type.set(
                self._get_or_create_choices(StairsTypeChoice, stairs_type_data)
            )
        if stairs_classification_data:
            instance.stairs_classification.set(
                self._get_or_create_choices(StairsClassificationChoice, stairs_classification_data)
            )
        if lighting_data:
            instance.lighting.set(
                self._get_or_create_choices(LightingTypeChoice, lighting_data)
            )
        if ventilation_data:
            instance.ventilation.set(
                self._get_or_create_choices(VentilationTypeChoice, ventilation_data)
            )
        if heating_data:
            instance.heating.set(
                self._get_or_create_choices(HeatingChoice, heating_data)
            )
        if security_data:
            instance.security.set(
                self._get_or_create_choices(SecurityChoice, security_data)
            )

        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        # Convert list fields to detailed representations
        # ret['external_walls_material'] = [{'id': item.id, 'name': item.name} for item in
        #                                   instance.external_walls_material.all()]
        # ret['inner_walls_material'] = [{'id': item.id, 'name': item.name} for item in
        #                                instance.inner_walls_material.all()]
        # ret['roof'] = [{'id': item.id, 'name': item.name} for item in instance.roof.all()]
        # ret['stairs_material'] = [{'id': item.id, 'name': item.name} for item in instance.stairs_material.all()]
        # ret['stairs_type'] = [{'id': item.id, 'name': item.name} for item in instance.stairs_type.all()]
        # ret['stairs_classification'] = [{'id': item.id, 'name': item.name, 'description': item.description}
        #                                 for item in instance.stairs_classification.all()]
        # ret['lighting'] = [{'id': item.id, 'name': item.name} for item in instance.lighting.all()]
        # ret['ventilation'] = [{'id': item.id, 'name': item.name} for item in instance.ventilation.all()]
        # ret['heating'] = [{'id': item.id, 'name': item.name} for item in instance.heating.all()]
        # ret['security'] = [{'id': item.id, 'name': item.name} for item in instance.security.all()]

        return ret