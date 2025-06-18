from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.datastructures import MultiValueDict

import auths.validators as a_validators
from helpers.serializers import (
    CategoryRetrieveField,
    FilesToDeleteRetrieveField,
)
from statements.models import (
    Statement,
    StatementMedia,
)
from auths.models import (
    Category,
)


class MyStatementSerializer(serializers.ModelSerializer):
    categories = CategoryRetrieveField(
        queryset=Category.objects.all(),
        many=True
        # , required=True
    )
    uploaded_media = serializers.ListField(
        child=serializers.FileField(
            write_only=True,
            required=False,
            validators=[a_validators.validate_files_extension]
        ),
        write_only=True,
        required=False,
        allow_empty=True,
    )
    files_to_delete = FilesToDeleteRetrieveField(
        queryset=StatementMedia.objects.all(),
        many=True,
        write_only=True,
        required=False,
        allow_empty=True,
    )

    class Meta:
        model = Statement
        fields = (
            'id',
            'categories',
            'text',
            'service_time',
            'location',
            'min_price',
            'max_price',
            'is_active',
            'files_to_delete',
            'uploaded_media',
        )

    def to_internal_value(self, data):
        """Handles multi-value-dict, like form-data."""
        if isinstance(data, MultiValueDict):
            if not 'uploaded_media' in data:
                data = data.copy()  # Make a mutable copy of the QueryDict
            categories = data.getlist('categories')
            files_to_delete = data.getlist('files_to_delete')
            if categories:
                data['categories'] = [int(cat.strip()) for cat in categories[0].split(',') if cat.strip()]
            if files_to_delete:
                data['files_to_delete'] = [int(file_id.strip()) for file_id in files_to_delete[0].split(',') if
                                           file_id.strip()]
        return super().to_internal_value(data)

    def update(self, statement, validated_data):
        uploaded_media = validated_data.pop('uploaded_media', [])
        files_to_delete = validated_data.pop('files_to_delete', [])
        categories_data_nested_array = validated_data.pop('categories', [])

        if files_to_delete and isinstance(files_to_delete[0], list):
            files_to_delete = files_to_delete[0]

        if 'categories' in validated_data:
            if categories_data_nested_array and isinstance(categories_data_nested_array[0], list):
                categories_data = categories_data_nested_array[0]
            else:
                categories_data = categories_data_nested_array
            category_ids = [category.id for category in categories_data]
            statement.categories.set(category_ids)
        statement = super().update(statement, validated_data)

        for media_to_delete in files_to_delete:
            if isinstance(media_to_delete, StatementMedia):
                media_to_delete.delete()
            elif isinstance(media_to_delete, int):
                try:
                    media = statement.media.all()[media_to_delete]
                    media.delete()
                except IndexError:
                    raise serializers.ValidationError({f"Media at index {media_to_delete} not found"})

        if uploaded_media:
            for media_file in uploaded_media:
                file_name = default_storage.get_available_name(media_file.name)
                try:
                    file_path = default_storage.save(file_name, ContentFile(media_file.read()))

                    StatementMedia.objects.create(statement=statement, file=media_file)
                except ValidationError as e:
                    default_storage.delete(file_path)
                    statement.delete()
                    raise serializers.ValidationError({"uploaded_media": str(e)})
        return statement

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request:
            representation['uploaded_media'] = [
                {
                    'id': media.id,
                    'file': request.build_absolute_uri(media.file.url),
                    'file_name': str(media.file)[16:],
                    'file_type': media.file_type,
                }
                for media in instance.media.all()
            ]
        return representation
