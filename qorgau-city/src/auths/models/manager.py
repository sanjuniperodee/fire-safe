import auths
from django.contrib.auth.base_user import BaseUserManager
from django.core.cache import cache
from django.core.exceptions import ValidationError
# from sms_gateway.mobizon.mobizon_api import MobizonApi
# from helpers.utils import generate_activation_code
from helpers.logger import log_message
from sms_gateway.smsc.smsc_utils import generate_sms_code, smsc_send_sms_code

from .role import (
    CustomUserRole,
    UserRole
)


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for creating and managing CustomUser instances.
    """

    def create_user(self, phone, password, **extra_fields):
        """
        Creates and saves a user with the given phone and password.
        Creates role 'CITIZEN' and adds it to CustomUser via UserRole model.

        Args:
        - phone (str): User's phone number.
        - password (str): User's password.
        - **extra_fields: Additional fields to save.

        Returns:
        - CustomUser: Created user instance.

        Raises:
        - ValidationError: If phone number is not provided or if the role is invalid.
        """
        if not phone:
            raise ValidationError("Phone Number is required")
        role = extra_fields.pop('role')

        if role and role not in dict(auths.Role.choices):
            raise ValidationError(f"Invalid role: {role}")

        user = self.model(
            phone=phone,
            password=password,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        user_role, created = CustomUserRole.objects.get_or_create(role=role)
        citizen_role, created = CustomUserRole.objects.get_or_create(role=auths.Role.CITIZEN)

        if user_role.role == auths.Role.INSPECTOR:
            UserRole.objects.create(user=user, role=user_role)
        else:
            UserRole.objects.create(user=user, role=user_role, status=auths.Status.ACCEPTED)

        if user_role != citizen_role and not user.is_inspector:
            UserRole.objects.create(user=user, role=citizen_role, status=auths.Status.ACCEPTED)

        # self.send_activation_sms(phone, user.id)

        return user

    # def send_activation_sms(self, phone, user_id):
    #     mobizon = MobizonApi()
    #     activation_code = generate_activation_code()
    #     cache_key = f'activation_code:{user_id}'
    #     result = cache.set(cache_key, activation_code)
    #     log_message(f'cache_key {cache_key}, '
    #                 f'code {activation_code}, '
    #                 f'result {result}')

    #     params = {
    #         'recipient': phone.replace("+", ""),
    #         'text': f'Код активации {activation_code}\n'
    #                 'ссылка на сайт https://qorgau-city.kz/',
    #     }
    #     mobizon.call('message', 'sendSMSMessage', **params)
    #     log_message(str(params))

    def send_activation_sms(self, phone, user_id):
        activation_code = generate_sms_code()
        cache_key = f'activation_code:{user_id}'
        result = cache.set(cache_key, activation_code)
        log_message(f'cache_key {cache_key}, '
                    f'code {activation_code}, '
                    f'result {result}')

        params = {
            'recipient': phone.replace("+", ""),
            'text': f'Код активации {activation_code}\n'
                    'ссылка на сайт https://qorgau-city.kz/',
        }
        smsc_send_sms_code(phone.replace("+", ""), activation_code)
        log_message(str(params))

    def create_superuser(self, phone, password, **extra_fields):
        user = self.create_user(phone, password, role='ADMIN', **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
