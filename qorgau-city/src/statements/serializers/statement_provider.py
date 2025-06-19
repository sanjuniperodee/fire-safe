from urllib import request

from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import ValidationError
from auths.models import CustomUser
from django.shortcuts import get_object_or_404
from statements import StatementStatus
from statements.models import (
    Statement,
    StatementProvider,
    StatementSuggestion,
)
from helpers.local_chat_api import create_statement_chat_room, change_statement_status
import auths


class StatementProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementProvider
        fields = [
            'id',
            'statement',
            'provider',
            'chat_room_id',
            'status',
            'archive_date',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'chat_room_id']

    def validate(self, attrs):
        statement = attrs.get('statement')
        provider = attrs.get('provider')

        # Check if this combination already exists
        existing = StatementProvider.objects.filter(
            statement=statement,
            provider=provider
        ).first()

        if existing:
            raise ValidationError(
                "Связь между этим заявлением и поставщиком уже существует."
            )

        return attrs

    def create(self, validated_data):
        statement = validated_data.get('statement')
        provider = validated_data.get('provider')

        # Check if statement exists and is active
        if not statement.is_active:
            raise ValidationError("Нельзя добавить поставщика к неактивной заявке.")

        with transaction.atomic():
            statement_provider = StatementProvider.objects.create(**validated_data)

            # Create chat room with local chat API (no JWT token needed)
            try:
                chat_room_id = create_statement_chat_room(
                    phone_1=statement.author.phone,
                    phone_2=provider.phone,
                    categories=list(statement.categories.values_list('id', flat=True)),
                    location=statement.location,
                    author_name=statement.author.first_name,
                    provider_name=provider.first_name,
                    statement_provider_id=statement_provider.id,
                    statement_id=statement.id
                )

                if chat_room_id:
                    statement_provider.chat_room_id = chat_room_id
                    statement_provider.save()
            except Exception as e:
                print(f'Failed to create chat room: {e}')
                # Don't fail the entire operation if chat room creation fails

        return statement_provider

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['phone'] = self.get_phone(instance)
        representation['chat_room_id'] = instance.chat_room_id
        return representation

    def get_phone(self, obj):
        return obj.statement.author.phone


class StatementProviderStatusSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=StatementStatus.choices)

    class Meta:
        model = StatementProvider
        fields = ['status']

    def validate_status(self, value):
        current_status = self.instance.status

        # Define valid transitions
        valid_transitions = {
            StatementStatus.OPENED: [StatementStatus.IN_WORK, StatementStatus.COMPLETED, StatementStatus.ARCHIVED],
            StatementStatus.IN_WORK: [StatementStatus.ARCHIVED, StatementStatus.COMPLETED],
            StatementStatus.COMPLETED: [],
            StatementStatus.ARCHIVED: []
        }

        if value not in valid_transitions.get(current_status, []):
            raise serializers.ValidationError(f"Invalid status transition from {current_status} to {value}")

        return value

    def validate(self, data):
        # First, call the parent's validate method
        data = super().validate(data)

        # Get the statement associated with this statement provider
        statement = self.instance.statement

        # Check if anyone else is working on this statement
        active_providers = StatementProvider.objects.filter(
            statement=statement,
            status__in=[StatementStatus.IN_WORK]
        ).exclude(id=self.instance.id)

        if active_providers.exists():
            raise serializers.ValidationError({
                "error": "Cannot change status because another provider is already working on this statement."
            })

        return data

    def update(self, instance, validated_data):
        new_status = validated_data['status']

        # Change status
        changed_status = change_statement_status(
            statement_id=instance.statement.id,
            status=new_status,
        )

        # If the new status is IN_WORK, set is_busy_by_provider to True
        statement = instance.statement

        if new_status == StatementStatus.IN_WORK or new_status == StatementStatus.COMPLETED:
            statement.is_busy_by_provider = True
        else:
            statement.is_busy_by_provider = False
        statement.save()
        instance.status = new_status
        instance.save()
        return instance


# class ProviderRetrieveField(serializers.PrimaryKeyRelatedField):
#     def to_representation(self, instance):
#         id = super().to_representation(instance)
#         author = Provider.objects.get(pk=id)
#         return ProviderSerializer(author).data