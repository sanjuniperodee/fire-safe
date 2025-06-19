import io
from rest_framework import viewsets, mixins, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from django.core.files.storage import default_storage
from helpers.logger import log_exception

from objects.models import (
    EvacAddress
)
from objects.serializers import (
    EvacAddressSerializer,
    EvacAddressListSerializer,
)


class EvacAddressViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [AllowAny, ]
    queryset = EvacAddress.objects.all()
    serializer_class = EvacAddressSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == 'list':
            serializer = EvacAddressListSerializer
        elif self.action == 'retrieve':
            serializer = EvacAddressListSerializer

        return serializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            object_name = serializer.validated_data['file_path'].name

            file = serializer.validated_data['file_path']
            file_content = file.read()
            file_obj = io.BytesIO(file_content)

            default_storage.save(object_name, file_obj)

            # Используем публичный endpoint для URL файла
            public_endpoint = getattr(settings, 'MINIO_PUBLIC_ENDPOINT', None) or settings.AWS_S3_ENDPOINT_URL
            file_path = f"{public_endpoint}/isec/{object_name}"
            serializer.validated_data['file_path'] = file_path
            serializer.validated_data['qrcode_url'] = f"{settings.QR_GENERATOR_LINK}&data={file_path}"

            self.perform_create(serializer)

            return Response(data={"qr_url": serializer.validated_data['qrcode_url']}, status=status.HTTP_201_CREATED)
        except Exception as e:
            log_exception(f"error: {str(e)}")
            return Response({"error": str(e)})
