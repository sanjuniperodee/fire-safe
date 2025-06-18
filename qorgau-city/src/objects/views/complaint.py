from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django_filters import rest_framework as django_filters
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from auths.models import MicroserviceJWTAuthentication

from objects.models import Complaint
from objects.serializers import (
    ComplaintListSerializer,
    ComplaintCreateSerializer,
    ComplaintDetailSerializer,
    ComplaintAnswerOutputSerializer,
)
from helpers import permissions
from helpers.chat_api import generate_jwt_token, delete_complaint_chat_room


class ComplaintFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Complaint._meta.get_field('status').choices)
    created_at = django_filters.DateTimeFromToRangeFilter()
    expiration_date = django_filters.DateTimeFromToRangeFilter()
    city = django_filters.CharFilter(lookup_expr='icontains')
    district = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Complaint
        fields = ['status', 'created_at', 'expiration_date', 'city', 'district']


class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    filter_backends = [django_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ComplaintFilter
    ordering_fields = ['created_at', 'expiration_date', 'status']
    ordering = ['-created_at']  # Default ordering

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [permissions.IsInspectorOrCitizen, ]
        elif self.action == 'mark_as_answered':
            permission_classes = [permissions.IsInspectorOnly, ]
        else:
            permission_classes = [permissions.IsCitizenOrReadOnly, ]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return ComplaintListSerializer
        elif self.action == 'create':
            return ComplaintCreateSerializer
        elif self.action == 'mark_as_answered':
            return ComplaintAnswerOutputSerializer
        return ComplaintDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Complaint.objects.all()
        elif user.is_inspector:
            return Complaint.objects.filter(inspector=user)
        else:
            return Complaint.objects.filter(author=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    @extend_schema(
        responses={
            204: OpenApiResponse(description="Complaint deleted successfully"),
            403: OpenApiResponse(description="Permission denied"),
            404: OpenApiResponse(description="Complaint not found"),
            409: OpenApiResponse(description="Cannot delete complaint in current state")
        },
        description="Delete a complaint. Only the author can delete their complaint, "
                    "and only if it's in PENDING status and within 24 hours of creation."
    )
    def destroy(self, request, *args, **kwargs):
        complaint = self.get_object()

        # Check complaint status
        # if complaint.status != 'PENDING':
        #     return Response(
        #         {"detail": "Only pending complaints can be deleted."},
        #         status=status.HTTP_409_CONFLICT
        #     )

        # Check if complaint is within 24 hours of creation
        # time_difference = timezone.now() - complaint.created_at
        # if time_difference.total_seconds() > 24 * 60 * 60:  # 24 hours in seconds
        #     return Response(
        #         {"detail": "Complaints can only be deleted within 24 hours of creation."},
        #         status=status.HTTP_409_CONFLICT
        #     )

        jwt_token = generate_jwt_token()

        print(f'complaint.chat_room_id is: {complaint.chat_room_id}')

        # Delete complaint chat room
        delete_complaint_chat_room(
            login_jwt_token=jwt_token,
            complaint_conversation_id=complaint.chat_room_id,
        )

        # Perform the deletion
        complaint.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(response=ComplaintAnswerOutputSerializer),
            403: OpenApiResponse(description="Permission denied")
        },
        description="Mark a complaint as answered",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="A unique integer value identifying this complaint"
            ),
        ]
    )
    @action(detail=True, methods=['post'])
    def mark_as_answered(self, request, pk=None):
        complaint = self.get_object()
        serializer = self.get_serializer(
            complaint,
            data={'status': 'ANSWERED'},
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        try:
            complaint.mark_as_answered()
            return Response(serializer.data)
        except ValueError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


# class ComplaintMicroServiceViewSet(viewsets.ModelViewSet):
#     """Complaint with Microservice auth."""
#     queryset = Complaint.objects.all()
#     authentication_classes = [MicroserviceJWTAuthentication]
#     serializer_class = ComplaintAnswerOutputSerializer
#     permission_classes = [AllowAny, ]
#     # Defining the allowed actions
#     http_method_names = ['post']
#
#     @extend_schema(
#         request=None,
#         responses={
#             200: OpenApiResponse(response=ComplaintAnswerOutputSerializer),
#             403: OpenApiResponse(description="Permission denied")
#         },
#         description="Mark a complaint as answered",
#         parameters=[
#             OpenApiParameter(
#                 name="id",
#                 type=OpenApiTypes.INT,
#                 location=OpenApiParameter.PATH,
#                 description="A unique integer value identifying this complaint"
#             ),
#         ]
#     )
#     @action(detail=True, methods=['post'])
#     def mark_as_answered(self, request, pk=None):
#         complaint = self.get_object()
#         complaint.mark_as_answered()
#         serializer = self.get_serializer(complaint)
#         return Response(serializer.data)
