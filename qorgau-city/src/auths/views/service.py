from datetime import datetime

from django.core.cache import cache
from drf_spectacular.utils import extend_schema, OpenApiParameter
from helpers.logger import log_message, log_exception
from helpers.utils import has_passed_30_minutes, send_sms_confirmation_code
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from auths.models import CustomUser
from auths.serializers import (
    PhoneSerializer,
    VerifySmsCodeSerializer,
)


class UserActivateView(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = CustomUser.objects.all()

    @extend_schema(
        parameters=[
            OpenApiParameter(name='code', type=int, location=OpenApiParameter.QUERY,
                             description='The code which is send to phone number'),
            OpenApiParameter(name='phone', type=int, location=OpenApiParameter.QUERY,
                             description='The phone number')
        ]
    )
    def get(self, request, *args, **kwargs):
        phone = request.GET.get('phone')
        code = request.GET.get('code')
        phone = phone.strip()
        phone = f"+{phone}" if "+" not in phone else phone
        user = CustomUser.objects.filter(phone=phone).first()

        log_message(f"phone {phone}, code {code}, user {user}")

        if user is not None:
            try_key = f'activation_try_{user.id}'
            activation_try = cache.get(try_key)

            try_time_key = f'activation_try_time_{user.id}'
            try_time = cache.get(try_time_key)

            if activation_try is None or has_passed_30_minutes(try_time):
                try_time_key = f'activation_try_time_{user.id}'
                activation_try = 1
                cache.set(try_time_key, datetime.now())

            if activation_try and activation_try > 3:
                return Response(
                    {"message": "Too many failed attempts, please try again after 30min"},
                    status=status.HTTP_200_OK
                )

            log_message(f"user {user}: try_time_key {try_time_key}, try_time {try_time}")

            cache_key = f'activation_code:{user.id}'
            activation_code = cache.get(cache_key)

            log_message(f"user {user}: activation_code {activation_code}, code {code}")
            if activation_code and code == activation_code:
                user.is_active = True
                user.save()
                return Response({"message": "User activated"}, status=status.HTTP_200_OK)
            activation_try += 1
            cache.set(try_key, activation_try)
        return Response({"message": "Activation code error"}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='phone', type=int, location=OpenApiParameter.QUERY,
                             description='The phone number to send activation code')
        ]
    )
    def resend(self, request, *args, **kwargs):
        phone = request.GET.get('phone')
        phone = phone.strip()
        phone = f"+{phone}" if "+" not in phone else phone
        code = send_sms_confirmation_code(phone)

        return Response({
            "message": "Activation code sended",
            "sms_code": code  # Временно возвращаем код для тестирования
        }, status=status.HTTP_200_OK)


class SendSmsCodeViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = PhoneSerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == 'verify_sms_code':
            serializer = VerifySmsCodeSerializer

        return serializer

    def send_sms_code(self, request, *args, **kwargs) -> Response:
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            code = send_sms_confirmation_code(serializer.data.get('phone'))

            return Response({
                "message": "SMS code sent successfully",
                "sms_code": code  # Временно возвращаем код для тестирования
            }, status=status.HTTP_200_OK)
        except Exception as e:
            log_exception(e, f'Failed to reset password {str(e)}')
            return Response(data=e.detail, status=status.HTTP_400_BAD_REQUEST)

    def verify_sms_code(self, request, *args, **kwargs) -> Response:
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            phone = serializer.data.get('phone')
            phone = phone.replace("+", "")
            code = serializer.data.get('code')
            cache_key = f'confirmation_code:{phone}'
            confirmation_code = cache.get(cache_key)
            log_message(f"cache_key {cache_key}, code {code}, confirmation_code {confirmation_code}")
            verified_key = f'verified_key:{phone}'
            if confirmation_code == code:
                cache.get(cache_key, None)
                result_v = cache.set(verified_key, True)
                log_message(f'verified_key {verified_key}, verify_sms_code {result_v}')
                return Response(status=status.HTTP_200_OK)

            cache.set(verified_key, False)
            return Response(data={"detail": f"Failed verify sms code {code}"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            log_exception(e, f'Failed verify sms code {str(e)}')
            return Response(data=e.detail, status=status.HTTP_400_BAD_REQUEST)
