from rest_framework import serializers
from django.core.exceptions import ValidationError

from objects.models import (
    Building,
    DocumentKeyFile,
    DocumentHistory,
)


class DocumentKeyListSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    comment = serializers.CharField()
    files = serializers.CharField()

    def to_representation(self, instance):
        return {
            "id": instance.get('id'),
            "title": instance.get('title'),
            "comment": instance.get('comment'),
            "comment_updated_date": instance.get('comment_updated_date'),
            "inspector_comment": instance.get('inspector_comment'),
            "inspector_comment_updated_date": instance.get('inspector_comment_updated_date'),
            "files": instance.get('files')
        }


class DocumentSubParagraphsSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    keys = DocumentKeyListSerializer(many=True, required=False)


class DocumentListSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    keys = DocumentKeyListSerializer(many=True, required=False)
    subParagraphs = DocumentSubParagraphsSerializer(many=True, required=False)


class DocumentKeyFileListSerializer(serializers.ModelSerializer):
    comment = serializers.CharField()

    class Meta:
        model = DocumentKeyFile
        fields = (
            'id',
            'path'
        )


class DocumentKeyFileCreateSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(required=False)
    building = serializers.PrimaryKeyRelatedField(
        queryset=Building.objects.all(), required=True)

    class Meta:
        model = DocumentKeyFile
        fields = (
            'building',
            'document_key',
            'path',
            'comment'
        )

    def create(self, validated_data):
        model = self.Meta.model
        path = validated_data.get('path', None)
        if path:
            file_name = path.name
        else:
            raise ValidationError("Path field is required.")
        validated_data['name'] = file_name
        instance = model.objects.create(**validated_data)

        return instance


class DocumentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentHistory
        fields = '__all__'


class DocumentKeyCreateOrUpdateSerializer(serializers.Serializer):
    document_id = serializers.IntegerField(required=True)
    title = serializers.CharField(required=True)
    organization_types = serializers.ListField(
        child=serializers.CharField(),
        required=True
    )

    def create(self, validated_data):
        """
        1) Ищем Document по document_id.
        2) get_or_create DocumentKey (title + document).
        3) Для каждого organization_type_name ищем (или создаем) OrganizationType, добавляем в M2M.
        """
        doc_id = validated_data['document_id']
        title = validated_data['title']
        org_type_names = validated_data['organization_types']

        # 1. Находим Document
        document = Document.objects.get(id=doc_id)

        # 2. Ищем или создаём DocumentKey
        key, created = DocumentKey.objects.get_or_create(
            title=title,
            document=document
        )

        # 3. Для каждого названия типа ищем (или создаем) OrganizationType
        for org_name in org_type_names:
            org_obj, _ = OrganizationType.objects.get_or_create(name=org_name)
            key.supported_organization_types.add(org_obj)

        return key

    def update(self, instance, validated_data):
        """
        Если хотите также поддерживать PATCH/PUT логику:
        - Можно здесь написать код обновления title, document_id и org.types
        """
        raise NotImplementedError("Обновление не реализовано в данном примере.")

    def to_representation(self, instance):
        """
        Опционально вернуть структуру данных, которая нужна вам на выходе.
        """
        return {
            "id": instance.id,
            "title": instance.title,
            "document_id": instance.document.id,
            "organization_types": [
                org.name for org in instance.supported_organization_types.all()
            ]
        }