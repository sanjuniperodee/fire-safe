import base64
import mimetypes
import os

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404  # Add this import
from drf_spectacular.utils import extend_schema, OpenApiParameter
from helpers.logger import log_exception
from helpers.utils import delete_file

from objects.models import Building, DocumentKey
from objects.models import (
    Building,
    DocumentKeyFile,
    DocumentComment,
    DocumentRemark,
)
from objects.serializers import (
    DocumentKeyFileCreateSerializer,
    DocumentHistorySerializer,
    DocumentKeyCreateOrUpdateSerializer,

    DocumentRemarkSerializer,
    DocumentRemarkCreateSerializer,
)
from objects.signals import document_keyfile_post_save


class DocumentKeyFileViewSet(viewsets.GenericViewSet):
    queryset = DocumentKeyFile.objects.select_related('building', 'document_key').all()
    serializer_class = DocumentKeyFileCreateSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'document_remark':
            return DocumentRemarkCreateSerializer
        elif self.action == 'get_remarks':
            return DocumentRemarkSerializer
        return DocumentKeyFileCreateSerializer

    @action(
        detail=False,
        methods=['post'],
        url_path='upload/file'
    )
    def upload_files(self, request, pk=None):
        try:
            data = request.data
            comment = data.pop('comment', None)
            building = data.get('building', None)

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            document_keyfile_post_save(instance, comment[0] if comment else '')
            if comment and comment is not None:
                exitst_comment = DocumentComment.objects.filter(document_key_id=data.get('document_key')).first()
                if exitst_comment:
                    exitst_comment.body = comment[0] if comment else ''
                    exitst_comment.building_id = building
                    exitst_comment.save()
                else:
                    DocumentComment.objects.create(
                        body=comment[0] if comment else '',
                        document_key_id=data.get('document_key'),
                        building_id=building
                    )

            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            log_exception(str(e))
            raise Http404

    @action(
        detail=True,
        methods=['get'],
        url_path='download/file'
    )
    def download_files(self, request, pk):
        obj = self.get_object()

        try:
            file_path = obj.path.name
            with default_storage.open(file_path, 'rb') as file:
                encoded_file = base64.b64encode(file.read()).decode('utf-8')
                mimetype, _ = mimetypes.guess_type(file_path)
                if not mimetype:
                    mimetype = 'application/octet-stream'

                response = HttpResponse(encoded_file, content_type=mimetype)
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
        except Exception as e:
            log_exception(f"File not found {str(e)}")
            return Response({"detail": "File not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(
        detail=True,
        methods=['delete'],
        url_path='delete/file'
    )
    def delete_fiels(self, request, pk):
        obj = self.get_object()
        path = obj.path.name
        obj.delete()
        delete_file(path)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['post'],
        url_path='document_remark'
    )
    def document_remark(self, request, pk=None):
        try:
            data = request.data
            serializer = DocumentRemarkSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

            return Response(
                DocumentRemarkSerializer(instance).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            log_exception(str(e))
            raise Http404

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='building',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Building ID to filter remarks',
                required=True
            )
        ]
    )
    @action(
        detail=True,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='get_remarks'
    )
    def get_remarks(self, request, pk=None):
        try:
            # document = self.get_object()  # This gets the document using pk from URL
            building_id = request.query_params.get('building')

            document = get_object_or_404(DocumentKey, id=pk) # DocumentKey.objects.get(pk=pk)
            building = get_object_or_404(Building, id=building_id)

            remarks = DocumentRemark.objects.filter(
                document_key=document,
                building=building
            ).order_by('-created_at')

            serializer = self.get_serializer(remarks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            log_exception(str(e))
            raise Http404


class BuildingHistoryViewSet(viewsets.GenericViewSet):
    queryset = Building.objects.prefetch_related('documents', 'histories').select_related('owner', 'organization_sub_type').all()
    serializer_class = DocumentHistorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(name='limit', type=int, location=OpenApiParameter.QUERY,
                             description='Number of results to return per page'),
            OpenApiParameter(name='offset', type=int, location=OpenApiParameter.QUERY,
                             description='The initial index from which to return the results')
        ]
    )
    @action(
        detail=True,
        methods=['get'],
        url_path='history'
    )
    def get_history(self, request, pk):
        try:
            obj = self.get_object()
            history = obj.histories.all()
            page = self.paginate_queryset(history)
            if page is not None:
                serializer = self.serializer_class(page, many=True)

                return self.get_paginated_response(serializer.data)

            serializer = self.serializer_class(history, many=True)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            log_exception(str(e))
            raise Http404


class DocumentKeyViewSet(viewsets.ModelViewSet):
    queryset = DocumentKey.objects.all()
    serializer_class = DocumentKeyCreateOrUpdateSerializer

    def create(self, request, *args, **kwargs):
        # Используем наш сериализатор
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        key = serializer.save()  # вызовет create(...)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
