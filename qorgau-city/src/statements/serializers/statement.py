from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.datastructures import MultiValueDict

from helpers.serializers import CategoryRetrieveField
import auths.validators as a_validators
from auths.serializers import (
    UserShortSerializer,
)
from auths.models import (
    Category,
)
from statements.models import (
    Statement,
    StatementMedia,
    StatementProvider,
)


class ObjectOwnerStatementSerializer(serializers.ModelSerializer):
    author = UserShortSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
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
        allow_empty=True
    )
    status = serializers.SerializerMethodField()
    is_seen = serializers.SerializerMethodField()
    is_called = serializers.SerializerMethodField()

    class Meta:
        model = Statement
        fields = (
            'id',
            'categories',
            'author',
            'text',
            'service_time',
            'location',
            'min_price',
            'max_price',
            'is_active',
            'status',
            'uploaded_media',
            'is_seen',
            'is_called',
            'created_at',
        )

    def get_status(self, obj):
        """Return status based on is_active and is_busy_by_provider fields"""
        if not obj.is_active:
            return 'ARCHIVED'
        elif obj.is_busy_by_provider:
            return 'IN_WORK'
        else:
            return 'OPENED'

    def get_is_seen(self, obj):
        user = self.context['request'].user
        if user.is_provider:
            return obj.is_seen_by(user)
        return None

    def get_is_called(self, obj):
        user = self.context['request'].user
        try:
            result = StatementProvider.objects.filter(statement=obj, provider=user).exists()
            print(f'get_is_called: Statement ID={obj.id}, User ID={user.id}, User phone={user.phone}, Result={result}')
            
            # Debug: Check all provider responses for this statement
            all_responses = StatementProvider.objects.filter(statement=obj)
            print(f'All provider responses for statement {obj.id}: {[f"Provider {sp.provider.id}({sp.provider.phone})" for sp in all_responses]}')
            
            return result
        except Exception as e:
            print(f'Error in get_is_called: {e}')
            return False

    def to_internal_value(self, data):
        """Handles multi-value-dict, like form-data."""
        if isinstance(data, MultiValueDict):
            if not 'uploaded_media' in data:
                # Make a mutable copy of the QueryDict
                data = data.copy()
            categories = data.getlist('categories')
            if categories:
                data['categories'] = [int(cat.strip()) for cat in categories[0].split(',') if cat.strip()]
        return super().to_internal_value(data)

    def create(self, validated_data):
        uploaded_media = validated_data.pop("uploaded_media", [])
        categories_data_nested_array = validated_data.pop('categories', [])
        if categories_data_nested_array and isinstance(categories_data_nested_array[0], list):
            categories_data = categories_data_nested_array[0]
        else:
            categories_data = categories_data_nested_array

        validated_data['is_active'] = True

        statement = Statement.objects.create(**validated_data)
        statement.categories.set(categories_data)

        for media_file in uploaded_media:
            try:
                StatementMedia.objects.create(statement=statement, file=media_file)
            except ValidationError as e:
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
                    'file_type': media.file_type
                }
                for media in instance.media.all()
            ]
        return representation
