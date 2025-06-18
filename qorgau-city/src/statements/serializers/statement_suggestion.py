from rest_framework import serializers
from auths.models import CustomUser
from statements.models import StatementSuggestion
from helpers.local_chat_api import create_statement_chat_room, change_statement_status


class ProviderListByCategorySerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'organization_name',
            'phone',
            'email',
            'last_name',
            'first_name',
            'middle_name',
            'categories',
        ]

    def get_categories(self, obj):
        return [
            {
                'id': category.id,
                'name': category.name,
                'measurement_unit': category.measurement_unit
            }
            for category in obj.provider_categories
        ]


class StatementSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementSuggestion
        fields = [
            'id',
            'statement',
            'provider',
            #'chat_room_id',
            'status',
            'archive_date',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        statement = attrs.get('statement')
        provider = attrs.get('provider')

        # Check if suggestion already exists
        existing_suggestion = StatementSuggestion.objects.filter(
            statement=statement,
            provider=provider
        ).first()

        if existing_suggestion:
            raise serializers.ValidationError(
                "You have already suggested this statement that you created to this provider."
            )
        return attrs

    def create(self, validated_data):
        # If we have an instance set during validation, update it
        if hasattr(self, 'instance') and self.instance:
            for attr, value in validated_data.items():
                setattr(self.instance, attr, value)
            self.instance.save()
            return self.instance

        # Otherwise create a new instance
        statement = validated_data['statement']
        provider = validated_data['provider']

        suggestion = StatementSuggestion.objects.create(**validated_data)

        # Create local chat room (no JWT token needed)
        try:
            chat_room_id = create_statement_chat_room(
                phone_1=statement.author.phone,
                phone_2=provider.phone,
                categories=list(statement.categories.values_list('id', flat=True)),
                location=statement.location,
                author_name=statement.author.first_name,
                provider_name=provider.first_name,
                statement_provider_id=suggestion.id,
                statement_id=statement.id
            )

            print(f'chat_room_id: {chat_room_id}')

            if chat_room_id:
                suggestion.chat_room_id = chat_room_id
                suggestion.save()
        except Exception as e:
            print(f'Failed to create chat room: {e}')
            # Don't fail the entire operation if chat room creation fails

        return suggestion

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['chat_room_id'] = instance.chat_room_id
        return representation