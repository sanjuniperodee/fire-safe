from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from objects.models import (
    Building,
    SubBuildingImage,
)
from objects.serializers import (
    SubBuildingImageSerializer,
    SubBuildingSerializer,
    MultipleSubBuildingImageUploadSerializer,
)


class SubBuildingViewSet(viewsets.ModelViewSet):
    # serializer_class = SubBuildingSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        # .list()
        # .retrieve()
        # .create()
        # .update()
        # .partial_update()
        # .destroy()
        if self.action in ['upload_images']:
            return MultipleSubBuildingImageUploadSerializer
        elif self.action in ['get_images']:
            return SubBuildingImageSerializer
        else:
            return SubBuildingSerializer

    def get_queryset(self):
        building = get_object_or_404(
            Building,
            pk=self.kwargs.get('building_id')
        )
        return building.subbuildings.all()

    def perform_create(self, serializer):
        building = get_object_or_404(
            Building,
            pk=self.kwargs.get('building_id')
        )
        serializer.save(building=building)

    @action(
        detail=True,
        methods=['post'],
        parser_classes=[MultiPartParser, FormParser],
        url_path='sub_building_images/upload'
    )
    def upload_images(self, request, building_id=None, pk=None):
        subbuilding = self.get_object()
        serializer = MultipleSubBuildingImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image_objects = serializer.save(subbuilding=subbuilding)
            response_serializer = SubBuildingImageSerializer(image_objects, many=True)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def upload_images(self, request, building_id=None, pk=None):
    #     subbuilding = self.get_object()
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(subbuilding=subbuilding)
    #         return Response(status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['get'],
        url_path='sub_building_images/list'
    )
    def get_images(self, request, building_id=None, pk=None):
        subbuilding = self.get_object()
        images = SubBuildingImage.objects.filter(subbuilding=subbuilding)
        serializer = self.get_serializer(images, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['delete'],
        url_path=r'sub_building_images/delete/(?P<image_id>\d+)',
    )
    def delete_image(self, request, building_id=None, pk=None, image_id=None):
        subbuilding = self.get_object()
        image = get_object_or_404(SubBuildingImage, id=image_id, subbuilding=subbuilding)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
