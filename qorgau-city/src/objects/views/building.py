from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from django.http import FileResponse
import mimetypes
import os

from helpers.permissions import IsInspectorOrReadOnly
import auths
from objects.models import (
    Building,
    Document,
    BuildingImage,
    BuildingRemark,
    EscapeLadderImage,
)
from objects.serializers import (
    BuildingCreateSerializer,
    BuildingDetailSerializer,
    BuildingListSerializer,
    MultipleBuildingImageUploadSerializer,
    BuildingImageSerializer,
    MultipleEscapeLadderImageUploadSerializer,
    EscapeLadderImageSerializer,

    BuildingRemarkCreateSerializer,
    BuildingRemarkSerializer,

    BuildingPDFDocumentSerializer,
)
from helpers.building_pdf_info_generator import BuildingPDFGenerator


class BuildingViewSet(viewsets.ModelViewSet):
    # add here permission in any way otherwise will be 403 error for no reason
    permission_classes = [IsAuthenticated]
    # queryset = Building.objects.prefetch_related(
    #     'documents').select_related('owner').all()
    queryset = Building.objects.prefetch_related(
        Prefetch('documents', queryset=Document.objects.order_by('id'))
    ).select_related('owner').all()
    #serializer_class = BuildingCreateSerializer

    # permission_classes = (IsObjectOwnerOrReadOnly,)
    def get_serializer_class(self):
        # .list()
        # .retrieve()
        # .create()
        # .update()
        # .partial_update()
        # .destroy()
        serializer = self.serializer_class
        if self.action == 'retrieve':
            serializer = BuildingDetailSerializer
        elif self.action == 'list':
            serializer = BuildingListSerializer
        elif self.action in ['remark', ]:
            return BuildingRemarkCreateSerializer
        elif self.action in ['get_remarks', ]:
            return BuildingRemarkSerializer
        elif self.action in ['upload_images']:
            serializer = MultipleBuildingImageUploadSerializer
        elif self.action in ['get_images']:
            serializer = BuildingImageSerializer
        elif self.action in ['upload_escape_ladder_images']:
            serializer = MultipleEscapeLadderImageUploadSerializer
        elif self.action in ['get_escape_ladder_images']:
            serializer = EscapeLadderImageSerializer
        elif self.action in ['generate_pdf']:
            serializer = None
        else:
            serializer = BuildingCreateSerializer
        return serializer

    def get_queryset(self):
        user = self.request.user
        # if isinstance(user, AnonymousUser):
        #     queryset = Building.objects.none()
        if user.is_superuser:
            queryset = super().get_queryset()
        else:
            user_roles = user.get_user_roles()
            match user_roles:
                case roles if auths.Role.OBJECT_OWNER in roles:
                    queryset = Building.objects.filter(owner=user)
                # case Role.INSPECTOR and Status.ACCEPTED:
                case auths.Role.INSPECTOR:
                    queryset = Building.objects.all()
                case roles if auths.Role.ADMIN in roles:
                    queryset = super().get_queryset()
                case _:
                    queryset = super().get_queryset()
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(
        methods=['patch'],
        detail=True,
        permission_classes=(IsInspectorOrReadOnly,)
    )
    def attach(self, request, pk):
        building = get_object_or_404(Building, id=pk)
        building.inspector = request.user
        building.save()
        serializer = BuildingListSerializer(building)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @attach.mapping.delete
    def delete_attach(self, request, pk):
        building = get_object_or_404(Building, id=pk)
        building.inspector = None
        building.save()
        serializer = BuildingListSerializer(building)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='limit', type=int, location=OpenApiParameter.QUERY,
                             description='Number of results to return per page'),
            OpenApiParameter(name='offset', type=int, location=OpenApiParameter.QUERY,
                             description='The initial index from which to return the results')
        ]
    )
    @action(
        methods=['get'],
        detail=False,
        permission_classes=(IsInspectorOrReadOnly,)
    )
    def my_objects(self, request):
        queryset = self.paginate_queryset(
            Building.objects.filter(inspector=request.user)
        )
        serializer = BuildingListSerializer(
            queryset, many=True,
            context={'request': request}
        )
        return self.get_paginated_response(
            serializer.data)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsInspectorOrReadOnly]
    )
    def remark(self, request, pk=None):
        building = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            remark = serializer.save(building=building, inspector=request.user)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                BuildingRemarkSerializer(remark).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def get_remarks(self, request, pk=None):
        building = self.get_object()
        remarks = BuildingRemark.objects.filter(building=building).order_by('-created_at')
        serializer = self.get_serializer(remarks, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['post'],
        parser_classes=[MultiPartParser, FormParser],
        url_path='building_images/upload'
    )
    def upload_images(self, request, pk=None):
        building = self.get_object()
        serializer = MultipleBuildingImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image_objects = serializer.save(building=building)
            response_serializer = BuildingImageSerializer(image_objects, many=True)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['get'],
        url_path='building_images/list'
    )
    def get_images(self, request, pk=None):
        building = self.get_object()
        images = BuildingImage.objects.filter(building=building)
        serializer = self.get_serializer(images, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], url_path=r'building_images/delete_image/(?P<image_id>\d+)')
    def delete_image(self, request, pk=None, image_id=None):
        building = self.get_object()
        image = get_object_or_404(BuildingImage, id=image_id, building=building)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post'],
        parser_classes=[MultiPartParser, FormParser],
        url_path='escape-ladder/upload'
    )
    def upload_escape_ladder_images(self, request, pk=None):
        building = self.get_object()
        serializer = MultipleEscapeLadderImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image_objects = serializer.save(building=building)
            response_serializer = EscapeLadderImageSerializer(image_objects, many=True)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['get'],
        url_path='escape-ladder/images'
    )
    def get_escape_ladder_images(self, request, pk=None):
        building = self.get_object()
        images = EscapeLadderImage.objects.filter(building=building)
        serializer = self.get_serializer(images, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['delete'],
        url_path=r'escape-ladder/delete/(?P<image_id>\d+)'
    )
    def delete_escape_ladder_image(self, request, pk=None, image_id=None):
        building = self.get_object()
        image = get_object_or_404(EscapeLadderImage, id=image_id, building=building)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post'],
        url_path='generate-pdf'
    )
    def generate_pdf(self, request, pk=None):
        building = self.get_object()

        # Delete existing PDF documents for this building
        existing_documents = building.pdf_documents.all()
        for doc in existing_documents:
            # Delete the actual file from storage
            if doc.file:
                doc.file.delete(save=False)
            # Delete the document record from database
            doc.delete()

        # Generate new PDF
        pdf_generator = BuildingPDFGenerator(building)
        pdf_document = pdf_generator.generate_and_save()

        # Get the file from storage
        file_obj = pdf_document.file

        # Create response with file
        response = FileResponse(
            file_obj.open('rb'),
            as_attachment=True,
            filename=os.path.basename(file_obj.name)
        )

        # Set content type
        content_type, _ = mimetypes.guess_type(file_obj.name)
        response['Content-Type'] = content_type or 'application/pdf'

        # Set content length
        response['Content-Length'] = file_obj.size

        # Set content disposition
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_obj.name)}"'

        return response

    @action(
        detail=True,
        methods=['get'],
        url_path='pdf-documents'
    )
    def list_pdf_documents(self, request, pk=None):
        building = self.get_object()
        pdf_documents = building.pdf_documents.all()
        serializer = BuildingPDFDocumentSerializer(
            pdf_documents,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)