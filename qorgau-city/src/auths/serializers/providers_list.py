from rest_framework import serializers
from auths.models import CustomUser, Category, UserCategory


class ProviderListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'last_name',
            'first_name',
            'middle_name',
            'phone',
            'email',
            'birthdate',
            'avatar_url',
            'iin',
            'bin_field',
            'main_organization_type',
            'company_name',
        ]


class ProviderDetailSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'last_name',
            'first_name',
            'middle_name',
            'phone',
            'email',
            'birthdate',
            'avatar_url',
            'iin',
            'actual_residence_address',
            'residence_address',
            'bin_field',
            'about_myself',
            'main_organization_type',
            'organization_type',
            'organization_sub_type',
            'organization_name',
            'company_name',
            'categories',
            'role'
        ]

    def get_categories(self, obj):
        provider_categories = obj.provider_categories
        return [
            {
                'id': category.id,
                'name': category.name,
                'measurement_unit': category.measurement_unit
            }
            for category in provider_categories
        ]

    def get_role(self, obj):
        return [role.role for role in obj.role.all()]