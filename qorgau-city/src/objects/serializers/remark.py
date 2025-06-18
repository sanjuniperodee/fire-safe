from rest_framework import serializers

from auths.serializers import UserShortSerializer
from objects.models import (
    Building,

    DocumentRemark,
    BuildingRemark,
)


class DocumentRemarkSerializer(serializers.ModelSerializer):
    """
    Serializer for reading DocumentRemark instances with nested related data.
    """
    building = serializers.PrimaryKeyRelatedField(queryset=Building.objects.all())
    # Add foreign key serializers for nested representation
    # inspector = UserShortSerializer(read_only=True)

    class Meta:
        model = DocumentRemark
        fields = [
            'id',
            'building',
            'document_key',
            'content',
            'created_at',
        ]
        read_only_fields = ['created_at']


class DocumentRemarkCreateSerializer(serializers.ModelSerializer):
    building = serializers.PrimaryKeyRelatedField(queryset=Building.objects.all(), required=True)

    class Meta:
        model = DocumentRemark
        fields = ('building', 'document_key', 'content')

    def create(self, validated_data):
        instance = DocumentRemark.objects.create(**validated_data)
        return instance


class BuildingRemarkSerializer(serializers.ModelSerializer):
    """
    Serializer for reading BuildingRemark instances with nested related data.
    """
    # inspector = UserMinimalSerializer(read_only=True)
    # building = BuildingMinimalSerializer(read_only=True)

    class Meta:
        model = BuildingRemark
        fields = [
            'id',
            'building',
            'inspector',
            'content',
            'created_at',
        ]
        read_only_fields = ['created_at']


class BuildingRemarkCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating BuildingRemark instances.
    """

    class Meta:
        model = BuildingRemark
        fields = [
            # 'building',
            'content',
        ]

    def create(self, validated_data):
        # Add the current user as the inspector
        validated_data['inspector'] = self.context['request'].user
        return super().create(validated_data)