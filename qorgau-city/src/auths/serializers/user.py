from django.utils.datastructures import MultiValueDict
from rest_framework import serializers

from auths.models import (
    CustomUser,
    CustomUserRole,
    UserRole,
    Category
)
from .profile import (
    EducationSerializer,
    ExperienceSerializer,
    AchievementSerializer,
    OtherAchievementSerializer
)
from .base import BaseUserSerializer
import auths
from helpers.serializers import CategoryRetrieveField


class UserSerializer(BaseUserSerializer):
    role = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = BaseUserSerializer.Meta.fields + (
            'birthdate',
            'role',
            'avatar_url',
            'actual_residence_address',
            'residence_address',
        )

    def get_role(self, obj):
        user_roles = UserRole.objects.filter(user=obj)
        return [{'role': user_role.role.role, 'status': user_role.status} for user_role in user_roles]


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'phone',
            'last_name',
            'first_name',
            'middle_name',
            'iin',
            'email'
        )


class InspectorSerializer(BaseUserSerializer):
    role = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = BaseUserSerializer.Meta.fields + (
            'rank',
            'position',
            'certificate_number',
            'birthdate',
            'role',
            'avatar_url',
            'inspector_jurisdiction_city',
            'inspector_jurisdiction_district',
        )

    def get_role(self, obj):
        user_roles = UserRole.objects.filter(user=obj)
        return [{'role': user_role.role.role, 'status': user_role.status} for user_role in user_roles]


class ObjectOwnerSerializer(BaseUserSerializer):
    role = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = BaseUserSerializer.Meta.fields + (
            'rank',
            'organization_name',
            'organization_type',
            'residence_address',
            'role',
        )

    def get_role(self, obj):
        user_roles = UserRole.objects.filter(user=obj)
        return [{'role': user_role.role.role, 'status': user_role.status} for user_role in user_roles]




class ProviderSerializer(BaseUserSerializer):
    role = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = BaseUserSerializer.Meta.fields + (
            'role',
            'residence_address',
            'organization_type',
            'bin_field',
            'categories',
        )

    def get_role(self, obj):
        user_roles = UserRole.objects.filter(user=obj)
        return [{'role': user_role.role.role, 'status': user_role.status} for user_role in user_roles]

    def get_categories(self, obj):
        # as indeces
        return list(obj.categories.values_list('id', flat=True))
        # as objects
        # return CategorySerializer(obj.categories.all(), many=True).data


class UserUpdateSerializer(BaseUserSerializer):
    iin = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    actual_residence_address = serializers.CharField(
        required=False,
        max_length=255
    )
    residence_address = serializers.CharField(
        required=False,
        max_length=255
    )
    #organization_type = serializers.CharField(required=False, allow_blank=True)
    organization_name = serializers.CharField(required=False, allow_blank=True)
    categories = CategoryRetrieveField(
        queryset=Category.objects.all(),
        many=True,
        required=True
    )
    inspector_jurisdiction_city = serializers.CharField(
        required=False,
        allow_blank=True
    )
    inspector_jurisdiction_district = serializers.CharField(
        required=False,
        allow_blank=True
    )

    class Meta:
        model = CustomUser
        fields = BaseUserSerializer.Meta.fields + (
            'about_myself',
            'birthdate',
            'avatar_url',
            'actual_residence_address',
            'residence_address',
            'rank',
            'position',
            'certificate_number',
            'main_organization_type',
            'organization_type',
            'organization_sub_type',
            'organization_name',
            'bin_field',
            'company_name',
            'categories',
            'inspector_jurisdiction_city',
            'inspector_jurisdiction_district',
        )
        extra_kwargs = {
            'last_name': {'required': True},
            'first_name': {'required': True},
            'middle_name': {'required': True},
            # 'categories': {'required': True},
        }

    def to_internal_value(self, data):
        """Handles multi-value-dict, like form-data."""
        if isinstance(data, MultiValueDict):
            categories = data.getlist('categories')
            if categories:
                data['categories'] = [int(cat.strip()) for cat in categories[0].split(',') if cat.strip()]
        return super().to_internal_value(data)

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories', None)
        if instance.is_provider:
            if categories_data is not None:
                category_ids = [category.id for category in categories_data[0]]
                instance.categories.set(category_ids)

            instance.main_organization_type = validated_data.get('main_organization_type', instance.organization_type)
            instance.organization_type = validated_data.get('organization_type', instance.organization_type)
            instance.organization_sub_type = validated_data.get('organization_sub_type', instance.organization_type)
            instance.organization_name = validated_data.get('organization_name', instance.organization_name)
            instance.bin_field = validated_data.get('bin_field', instance.bin_field)
            instance.company_name = f"{instance.organization_type} {instance.organization_name}".strip()

        elif instance.is_inspector:
            instance.rank = validated_data.get('rank', instance.rank)
            instance.position = validated_data.get('position', instance.position)
            instance.certificate_number = validated_data.get('certificate_number', instance.certificate_number)
            instance.inspector_jurisdiction_city = validated_data.get('inspector_jurisdiction_city',
                                                                      instance.inspector_jurisdiction_city)
            instance.inspector_jurisdiction_district = validated_data.get('inspector_jurisdiction_district',
                                                                          instance.inspector_jurisdiction_district)
        else:
            validated_data.pop('main_organization_type', None)
            validated_data.pop('organization_type', None)
            validated_data.pop('organization_sub_type', None)
            validated_data.pop('organization_name', None)
            validated_data.pop('rank', None)
            validated_data.pop('position', None)
            validated_data.pop('certificate_number', None)
            validated_data.pop('inspector_jurisdiction_city', None)
            validated_data.pop('inspector_jurisdiction_district', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserRoleUpdateSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=auths.Role.choices, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'role',
        ]


class UserAvatarUploadSerializer(serializers.ModelSerializer):
    avatar_url = serializers.FileField()

    class Meta:
        model = CustomUser
        fields = (
            "avatar_url",
        )