import auths
from auths.models import CustomUser, Category
from django.http import Http404
from helpers.local_chat_api import register_user_to_chat
from helpers.logger import log_exception
from helpers.serializers import CategoryRetrieveField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
import requests

from .base import BaseUserSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор для создания токена авторизации."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['phone'] = user.phone

        return token


class ResetPasswordSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = (
            'phone',
            'old_password',
            'new_password',
            'confirm_password',
        )

    def create(self, validated_data):
        phone = validated_data.get('phone')
        phone = f"+{phone}" if "+" not in phone else phone
        old_password = validated_data.get('old_password')
        new_password = validated_data.get('new_password')

        user = CustomUser.objects.filter(phone=phone).first()
        if user and user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return user
        raise serializers.ValidationError({"old_password": "Не правильный пароль"})

    def validate(self, data):
        if data['new_password'] == data['old_password']:
            raise serializers.ValidationError({"new_password": "Новый пароль не должен совпадать с текущим паролем"})
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"new_password": "Пароли не совпадают"})
        return data


class ForgotPasswordSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = (
            'phone',
            'password',
        )

    def create(self, validated_data):
        phone = validated_data.get('phone', None)
        password = validated_data.get('password', None)
        user = CustomUser.objects.get(phone=phone)
        if user and password:
            user.set_password(password)
            user.save()
            return user
        log_exception(f"phone {phone} pas {password}")
        raise Http404


class UserRegisterSerializer(BaseUserSerializer):
    """Сериализатор для регистрации пользователя."""

    role = serializers.ChoiceField(
        choices=auths.Role.choices,
        required=True
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    birthdate = serializers.DateField(
        required=True
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )
    actual_residence_address = serializers.CharField(
        required=False,
        max_length=255
    )
    residence_address = serializers.CharField(
        required=False,
        max_length=255
    )

    organization_type = serializers.CharField(
        required=False,
        allow_blank=True
    )
    organization_name = serializers.CharField(
        required=False,
        allow_blank=True
    )
    categories = CategoryRetrieveField(
        queryset=Category.objects.all(),
        many=True,
        required=False
    )
    inspector_jurisdiction_city = serializers.CharField(
        required=False,
        allow_blank=True
    )
    inspector_jurisdiction_district = serializers.CharField(
        required=False,
        allow_blank=True
    )

    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = BaseUserSerializer.Meta.fields + (
            'actual_residence_address',
            'residence_address',
            'rank',
            'position',
            'certificate_number',
            'birthdate',
            'role',
            'password',
            'password2',
            #'organization_type',
            'main_organization_type',
            'organization_type',
            'organization_sub_type',
            'organization_name',
            'bin_field',
            'categories',
            'inspector_jurisdiction_city',
            'inspector_jurisdiction_district',
        )
        extra_kwargs = {
            'last_name': {'required': True},
            'first_name': {'required': True},
            'middle_name': {'required': True},
            'bin_field': {'required': False},
        }

    def validate_passwords(self, attrs, password2):
        if attrs['password'] != password2:
            raise serializers.ValidationError(
                {'password': 'Пароли не совпадают'}
            )
        return attrs

    def validate_phone(self, value):
        if CustomUser.objects.filter(phone=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким номером телефона уже существует'
            )
        return value

    def validate_role(self, value):
        allowed_roles = [auths.Role.CITIZEN, auths.Role.OBJECT_OWNER, auths.Role.INSPECTOR, auths.Role.PROVIDER]
        if value not in allowed_roles:
            raise serializers.ValidationError("Invalid role for registration.")
        return value

    def validate(self, data):
        validated_data = super().validate(data)

        if data.get('role') == auths.Role.PROVIDER:
            organization_name = data.get('organization_name')
            organization_type = data.get('organization_type')
            if organization_name:
                if CustomUser.objects.filter(
                        organization_name=organization_name).exists() and CustomUser.objects.filter(
                    organization_type=organization_type).exists():
                    raise serializers.ValidationError({
                        "organization_name": "A provider with this organization name and organization type already exists. Please choose a different name and type."
                    })

            iin = data.get('iin')
            if iin and CustomUser.objects.filter(bin_field=iin).exists():
                raise serializers.ValidationError({
                    "iin": "A provider with this BIN already exists."
                })

        return validated_data

    def create(self, validated_data):
        password2 = validated_data.pop('password2')
        self.validate_passwords(validated_data, password2)

        exclude_user_fields = ['main_organization_type', 'organization_type', 'organization_sub_type',
                               'organization_name', 'categories',
                               'bin_field',
                               'rank', 'position', 'certificate_number', 'inspector_jurisdiction_city',
                               'inspector_jurisdiction_district',
                               'actual_residence_address', 'residence_address']
        user_data = {k: v for k, v in validated_data.items() if k not in exclude_user_fields}

        # Create user with create_user method (it already sets password)
        user = CustomUser.objects.create_user(**user_data)
        # Don't call user.set_password() again - it's already done in create_user

        # Register to local chat system - no external service needed
        registration_key = register_user_to_chat(validated_data['phone'], validated_data['password'])
        already_registered = False  # Всегда успешно для локального чата

        if validated_data['role'] == auths.Role.PROVIDER:
            user.actual_residence_address = validated_data.get('actual_residence_address', '')
            user.residence_address = validated_data.get('residence_address', '')
            user.main_organization_type = validated_data.get('main_organization_type', '')
            user.organization_type = validated_data.get('organization_type', '')
            user.organization_sub_type = validated_data.get('organization_sub_type', '')
            user.organization_name = validated_data.get('organization_name', '')
            if user.organization_type and user.organization_name:
                user.company_name = user.organization_type + ' ' + user.organization_name
            user.bin_field = validated_data.get('bin_field', '')
            
            # Handle categories safely
            categories_data = validated_data.get('categories', [])
            if categories_data:
                category_ids = [category.id for category in categories_data]
                user.categories.set(category_ids)
                
        elif validated_data['role'] == auths.Role.INSPECTOR:
            user.rank = validated_data.get('rank', '')
            user.position = validated_data.get('position', '')
            user.certificate_number = validated_data.get('certificate_number', '')
            user.inspector_jurisdiction_city = validated_data.get('inspector_jurisdiction_city', '')
            user.inspector_jurisdiction_district = validated_data.get('inspector_jurisdiction_district', '')
        else:
            user.actual_residence_address = validated_data.get('actual_residence_address', '')
            user.residence_address = validated_data.get('residence_address', '')

        user.is_active = True
        user.save()

        response_data = self.to_representation(user)
        response_data['already_registered_in_chat'] = already_registered
        # response_data['already_registered_in_chat'] = False
        return response_data