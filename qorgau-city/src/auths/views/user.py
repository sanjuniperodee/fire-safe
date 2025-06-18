from django.shortcuts import get_object_or_404
from helpers.logger import log_exception
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auths.models import (
    CustomUser,
    CustomUserRole,
    UserRole
)
from auths.serializers import (
    UserSerializer,
    UserAvatarUploadSerializer,
    UserUpdateSerializer,
    UserRoleUpdateSerializer,
    InspectorSerializer,
    ProviderSerializer,
    ObjectOwnerSerializer,

    ProviderListSerializer,
    ProviderDetailSerializer,
)
import auths

from helpers import permissions


class UserViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAuthenticated,)
    # allowed_methods = ['GET', 'POST']

    def get_permissions(self):
        if self.action in ['provider_list', 'provider_detail']:
            permission_classes = [permissions.IsInspectorOnly, ]
        else:
            permission_classes = [IsAuthenticated, ]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == 'update':
            serializer = UserUpdateSerializer
        elif self.action == 'partial_update':
            serializer = UserUpdateSerializer
        elif self.action == 'user_roles':
            serializer = UserRoleUpdateSerializer
        elif self.action == 'provider_list':
            serializer = ProviderListSerializer
        elif self.action == 'provider_detail':
            serializer = ProviderDetailSerializer
        return serializer

    @action(detail=False, methods=['patch'], parser_classes=[JSONParser])
    def user_roles(self, request, *args, **kwargs):
        """
        Add a role to the authenticated user.
        This method allows an authenticated user to add a new role to their account. It checks if the specified role is valid,
        and if the user does not already have this role. It then assigns the role to the user based on certain conditions.
        """
        user = request.user
        new_role_name = request.data.get('role')

        if new_role_name not in auths.Role.values:
            return Response(
                {
                    'error': 'Invalid role name'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_role = CustomUserRole.objects.get(role=new_role_name)
        can_add_accepted = (
                (user.is_citizen and new_role.can_add_object_owner) or
                (user.is_citizen and new_role.can_add_provider) or
                (user.is_provider and new_role.can_add_object_owner) or
                (user.is_object_owner and new_role.can_add_provider) or
                (new_role.can_add_citizen)
        )

        if not user.role.filter(role=new_role_name).exists():
            if can_add_accepted:
                UserRole.objects.create(
                    user=user, role=new_role,
                    status=auths.Status.ACCEPTED,
                )
            else:
                return Response(
                    {
                        "error": "User role cannot be created "
                                 "for current user due to role restrictions.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {
                    "error": "User already has the specified role.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                'success': 'User role successfully created for current user.',
            },
            status=status.HTTP_200_OK,
        )

    @user_roles.mapping.delete
    def delete_user_role(self, request, *args, **kwargs):
        """
        Remove a role from the authenticated user.

        This method allows an authenticated user to remove a role from their account. It checks if the specified role exists
        and if the user has this role before removing it.
        """
        user = request.user
        serializer = UserRoleUpdateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        role_name = serializer.validated_data['role']

        if role_name not in auths.Role.values:
            return Response(
                {'error': 'Invalid role name'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user_role = UserRole.objects.filter(user=user, role__role=role_name).first()

        if user_role:
            if (not user.has_single_role):
                if user_role.status == auths.Status.ACCEPTED:
                    other_accepted_roles = user.user_roles.filter(
                        status=auths.Status.ACCEPTED
                    ).exclude(
                        id=user_role.id
                    )

                    if other_accepted_roles.exists():
                        user_role.delete()
                        return Response(
                            {'success': 'User role deleted successfully.'},
                            status=status.HTTP_204_NO_CONTENT
                        )
                    else:
                        return Response(
                            {
                                'error': 'Cannot delete the only accepted role. '
                                         'User must have at least one accepted role.'
                            },
                            status=status.HTTP_400_BAD_REQUEST),
                else:
                    user_role.delete()
                    return Response(
                        {
                            'success': 'User role deleted successfully.'
                        },
                        status=status.HTTP_204_NO_CONTENT,
                    )
            else:
                return Response(
                    {
                        'error': 'User can not have less than one role.'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {
                    'error': 'User does not have the specified role.'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        if 'avatar_url' in data:
            data.pop('avatar_url')
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        if instance.is_provider:
            response_serializer = ProviderSerializer(instance)
        elif instance.is_inspector:
            response_serializer = InspectorSerializer(instance)
        elif instance.is_object_owner:
            response_serializer = ObjectOwnerSerializer(instance)
        else:
            response_serializer = UserUpdateSerializer(instance)
        return Response(response_serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def provider_list(self, request):
        """
        List all users with provider role.
        Returns a list of all users who have the PROVIDER role.
        """
        providers = CustomUser.objects.filter(
            role__role='PROVIDER'
        ).distinct()

        page = self.paginate_queryset(providers)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(providers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def provider_detail(self, request, pk=None):
        """
        Retrieve a specific provider user by ID.
        Returns detailed information about a specific provider user.
        """
        user = self.get_object()

        if not user.is_provider:
            return Response(
                {'error': 'User is not a provider'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(user)
        return Response(serializer.data)


class UserMeViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.user.is_inspector:
            return InspectorSerializer
        elif self.request.user.is_provider:
            return ProviderSerializer
        else:
            return UserSerializer

    @action(
        methods=['GET'],
        detail=False,
        url_path='me'
    )
    def me(self, requests, *args, **kwargs) -> Response:
        if self.request.user.is_authenticated:
            try:
                user = self.request.user
                serializer = self.get_serializer(user)
                return Response(serializer.data)
            except Exception as e:
                log_exception(e, 'Error user me')

        return Response(status=status.HTTP_404_NOT_FOUND)


class AvatarViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserAvatarUploadSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == 'delete_avatar':
            serializer = None

        return serializer

    @action(
        detail=True,
        methods=['post'],
        url_path='upload'
    )
    def upload_avatar(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = self.serializer_class(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['delete'],
        url_path='delete'
    )
    def delete_avatar(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.avatar_url.delete(save=True)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
