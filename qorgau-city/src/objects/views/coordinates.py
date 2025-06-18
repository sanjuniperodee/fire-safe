from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import Http404
from helpers.logger import log_exception

from objects.models import (
    Building,
    BuildingCoordinates
)
from objects.serializers import (
    BuildingCoordinatesSerializer,
    BuildingCoordinatesFullySerializer,
)


class BuildingCoordinateViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = BuildingCoordinates.objects.all()
    serializer_class = BuildingCoordinatesSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def list(self, request, *args, **kwargs):
        self.pagination_class = None
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='full')
    def get_full_coordinates(self, request, pk=None):
        try:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = BuildingCoordinatesFullySerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = BuildingCoordinatesFullySerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            log_exception(str(e))
            raise Http404

    @action(detail=True, methods=['get'], url_path='full')
    def get_building_full_coordinates(self, request, pk):
        try:
            building = Building.objects.filter(id=pk).first()
            coordinates = building.coordinates.all().first()
            serializer = BuildingCoordinatesFullySerializer(coordinates)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            log_exception(str(e))
            raise Http404
