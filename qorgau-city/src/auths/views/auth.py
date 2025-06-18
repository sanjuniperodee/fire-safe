from django.core.cache import cache
from helpers.logger import log_message, log_exception
from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from auths.models import CustomUser
from auths.serializers import (
    UserRegisterSerializer,
    UserSerializer,
    ResetPasswordSerializer,
    ForgotPasswordSerializer,
    MyTokenObtainPairSerializer,
)


class UserRegisterView(generics.CreateAPIView):
    """Register Citizen or Object Owner."""

    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        role = request.data.get('role')
        user_data = serializer.save(role=role)

        if isinstance(user_data, dict):
            user = CustomUser.objects.get(id=user_data['id'])
            response_data = UserSerializer(user).data
            response_data['already_registered_in_chat'] = user_data['already_registered_in_chat']
        else:
            user = user_data
            response_data = UserSerializer(user).data
            response_data['already_registered_in_chat'] = False  # Default value

        headers = self.get_success_headers(response_data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class MyObtainTokenPairView(TokenObtainPairView):
    """LoginView тип."""

    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class ResetPasswordViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ResetPasswordSerializer
    permission_classes = (IsAuthenticated,)

    def reset_password(self, request, *args, **kwargs) -> Response:
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            log_exception(e, f'Failed to reset password {str(e)}')
            return Response(data=e.detail, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ForgotPasswordSerializer
    permission_classes = []
    authentication_classes = []

    def forgot_password(self, request, *args, **kwargs) -> Response:
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            phone = request.data.get('phone')
            phone = phone.replace("+", "")

            verified_key = f"verified_key:{phone}"
            verified_cache = cache.get(verified_key)
            log_message(f'verified_key {verified_key}, verified_cache {verified_cache}')
            if verified_cache:
                serializer.save()
                return Response(status=status.HTTP_200_OK)

            return Response(
                data={
                    "detail": "You are not verified by SMS code",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            log_exception(e, f'Failed to reset password {str(e)}')
            return Response(data=e.detail, status=status.HTTP_400_BAD_REQUEST)
