from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter

from statements import StatementStatus
from auths.models import (
    UserCategory,
    CustomUser,
)
from helpers.filters import (
    StatementFilter,
    BooleanOrderingFilter,
)
from helpers.permissions import (
    IsAuthorOrReadOnly,
    IsProviderOrReadOnly,
    IsObjectOwner,
)
from helpers.local_chat_api import create_statement_chat_room
from statements.models import (
    Statement,
    StatementProvider,
    SeenStatement,
)
from statements.serializers import (
    ObjectOwnerStatementSerializer,
    MyStatementSerializer,
    StatementProviderSerializer,
    StatementProviderStatusSerializer,

    ProviderListByCategorySerializer,
    StatementSuggestionSerializer,
)


class StatementViewSet(viewsets.ModelViewSet):
    queryset = Statement.objects.all()
    serializer_class = ObjectOwnerStatementSerializer
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, BooleanOrderingFilter)
    filterset_class = StatementFilter
    ordering_fields = ['created_at', 'seen', 'seen_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsObjectOwner]
        elif self.action == ['update', 'partial_update', 'destroy']:
            permission_classes = [IsObjectOwner]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthorOrReadOnly]
        elif self.action == 'call_statement':
            permission_classes = [IsProviderOrReadOnly]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update', 'my_statement_id']:
            return MyStatementSerializer
        elif self.action == 'call_statement':
            return StatementProviderSerializer
        elif self.action == 'suggest_statement':
            return StatementSuggestionSerializer
        elif self.action == 'change_statement_provider_status':
            return StatementProviderStatusSerializer
        elif self.action == 'get_matching_providers':
            return ProviderListByCategorySerializer
        return ObjectOwnerStatementSerializer

    def get_queryset(self):
        """
        Returns statements based on the user's role:
        - If the user is a provider, returns active statements
          whose categories intersect with the provider's categories,
          excluding the provider's own statements.
        - If the user is not a provider, returns active statements authored by the user.
        """
        if self.action in ['update', 'partial_update', 'retrieve', 'destroy']:
            return Statement.objects.filter(is_active=True)
        if self.request.user.is_provider:
            provider_categories = UserCategory.objects.filter(user=self.request.user)
            category_ids = provider_categories.values_list('category_id', flat=True)
            queryset = Statement.objects.filter(
                categories__in=category_ids,
                is_active=True,
                is_busy_by_provider = False,
            ).exclude(author=self.request.user).distinct()
        else:  # elif self.request.user.is_object_owner:
            queryset = Statement.objects.filter(author=self.request.user, is_active=True)
        return queryset.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).distinct()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        statement = Statement.objects.get(pk=kwargs['pk'])
        if request.user.is_provider:
            SeenStatement.objects.get_or_create(
                user=request.user,
                statement=statement,
            )

        serializer = self.get_serializer(statement)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='limit', type=int, location=OpenApiParameter.QUERY,
                description='Number of results to return per page',
            ),
            OpenApiParameter(
                name='offset', type=int, location=OpenApiParameter.QUERY,
                description='The initial index from which to return the results',
            )
        ]
    )
    @action(
        methods=['get'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def my_statements(self, request):
        queryset = Statement.objects.filter(
            author=request.user,
            is_active=True,
        ).distinct().order_by('-created_at')
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(
                page, many=True,
                context={
                    'request': request,
                }
            )
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(
            queryset, many=True,
            context={
                'request': request,
            }
        )
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='my_statements/(?P<pk>[^/.]+)',
        permission_classes=(IsAuthenticated,)
    )
    def my_statement_id(self, request, pk=None):
        statement = get_object_or_404(
            Statement,
            pk=pk,
            author=request.user,
        )

        if request.method == 'GET':
            serializer = self.get_serializer(
                statement,
                context={
                    'request': request,
                }
            )
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = self.get_serializer(
                statement,
                data=request.data,
                partial=True,
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(
        detail=False,
        # methods=['post', 'delete'],
        methods=['post'],
        url_path='response/call/(?P<statement_id>[^/.]+)',
        parser_classes=[JSONParser],
        permission_classes=[IsProviderOrReadOnly],
    )
    def call_statement(self, request, statement_id=None):
        if request.method == 'POST':
            try:
                # Combine the statement_id from the URL with the request data
                data = request.data.copy()
                data['statement'] = statement_id
                data['provider'] = request.user.id  # Автоматически добавляем текущего пользователя как провайдера

                print(f'=== call_statement called ===')
                print(f'Statement ID: {statement_id}')
                print(f'Provider ID: {request.user.id}')
                print(f'Request data: {data}')

                serializer = self.get_serializer(data=data)
                if serializer.is_valid():
                    print('Serializer is valid, calling save()')
                    statement_provider = serializer.save()
                    print(f'StatementProvider created successfully: {statement_provider.id}')
                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    print(f'Serializer validation errors: {serializer.errors}')
                    return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except Exception as e:
                print(f'Error in call_statement: {e}')
                import traceback
                traceback.print_exc()
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

    @action(
        detail=False,
        methods=['post'],
        url_path='response/suggest/(?P<statement_id>[^/.]+)',
        parser_classes=[JSONParser],
        # permission_classes=[IsAuthenticated]  # Or any other appropriate permission
    )
    def suggest_statement(self, request, statement_id=None):
        """
        Allows statement authors to suggest their statement to specific providers.
        """
        # Combine the statement_id and provider from the request data
        data = request.data.copy()
        data['statement'] = statement_id

        serializer = StatementSuggestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['patch'])
    def change_statement_provider_status(self, request, pk=None):
        try:
            # print(f'StatementProvider: {StatementProvider.objects.get(statement__id=pk).id}')
            # statement_provider_id = StatementProvider.objects.get(statement__id=pk).id
            #
            # statement_provider = StatementProvider.objects.get(statement__id=pk) # , provider=request.user
            statement_provider_id = pk
            statement_provider = StatementProvider.objects.get(id=pk)  # , provider=request.user
        except StatementProvider.DoesNotExist:
            return Response({'error': 'StatementProvider not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(statement_provider, data=request.data, partial=True,
                                         context={
                                             'request': request,
                                             'statement_provider_id': statement_provider_id  # Pass the pk to the serializer
                                         }
                                         )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(
        detail=False,
        methods=['get'],
        url_path='response/selected',
        permission_classes=[IsProviderOrReadOnly]
    )
    def selected_statements(self, request):
        print(f'=== selected_statements called ===')
        print(f'User: {request.user.id} ({request.user.phone})')
        
        queryset = Statement.objects.filter(
            provider_responses__provider=request.user,
        )
        
        print(f'Found {queryset.count()} statements for user')
        for stmt in queryset:
            print(f'Statement {stmt.id}: responses={stmt.provider_responses.count()}')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True,
            )
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(
            queryset, many=True,
        )
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['get'],
        url_path='response/called'
    )
    def called_statements(self, request):
        queryset = Statement.objects.filter(
            author=request.user,
            provider_responses__isnull=False,
        ).distinct()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True,
            )
            data = serializer.data
            for item in data:
                statement = next(
                    s for s in page if s.id == item['id']
                )
                item['providers'] = self.get_providers(statement)
            return self.get_paginated_response(data)
        serializer = self.get_serializer(
            queryset, many=True,
        )
        data = serializer.data
        for item in data:
            statement = next(
                s for s in queryset if s.id == item['id']
            )
            item['providers'] = self.get_providers(statement)
        return Response(data)

    def get_providers(self, statement):
        return [
            {
                'id': sp.provider.id,
                'organization_name': sp.provider.organization_name,
                'user_id': sp.provider.id,
                'phone': sp.provider.phone,
                'last_name': sp.provider.last_name,
                'first_name': sp.provider.first_name,
                'middle_name': sp.provider.middle_name,
                'email': sp.provider.email,
            }
            for sp in statement.provider_responses.select_related('provider')
        ]

    @action(
        detail=True,
        methods=['get'],
        url_path='matching-providers',
        #permission_classes=[IsAuthenticated]
    )
    def get_matching_providers(self, request, pk=None):
        """
        Returns a list of providers that have matching categories with the statement.
        """
        try:
            statement = Statement.objects.get(pk=pk)
            # Get the categories associated with the statement
            statement_categories = statement.categories.all()

            # provider_categories = UserCategory.objects.filter(user=self.request.user)
            # category_ids = provider_categories.values_list('category_id', flat=True)
            # queryset = Statement.objects.filter(
            #     categories__in=category_ids,
            #     is_active=True,
            # ).exclude(author=self.request.user).distinct()

            # Find providers who have at least one matching category
            matching_providers = CustomUser.objects.filter(
                role__role='PROVIDER',  # Filter users with provider role
                is_active=True,  # Only active providers
                user_categories__category__in=statement_categories,  # Match categories
                user_categories__role='PROVIDER'  # Ensure we're matching provider categories
            ).distinct()

            # Exclude the statement author if they happen to be a provider
            matching_providers = matching_providers.exclude(id=statement.author.id)

            # Paginate the results
            page = self.paginate_queryset(matching_providers)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(matching_providers, many=True)
            return Response(serializer.data)

        except Statement.DoesNotExist:
            return Response(
                {'error': 'Statement not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(
        detail=True,
        methods=['get'],
        url_path='debug'
    )
    def debug_statement(self, request, pk=None):
        """Debug endpoint to check statement provider status"""
        try:
            statement = Statement.objects.get(pk=pk)
            
            debug_info = {
                'statement_id': statement.id,
                'statement_status': statement.status,
                'statement_author': {
                    'id': statement.author.id,
                    'phone': statement.author.phone,
                    'name': f"{statement.author.first_name} {statement.author.last_name}".strip()
                },
                'current_user': {
                    'id': request.user.id,
                    'phone': request.user.phone,
                    'name': f"{request.user.first_name} {request.user.last_name}".strip(),
                    'is_provider': request.user.is_provider
                },
                'provider_responses': [],
                'chat_rooms': []
            }
            
            # Get all provider responses
            for sp in statement.provider_responses.all():
                debug_info['provider_responses'].append({
                    'id': sp.id,
                    'provider_id': sp.provider.id,
                    'provider_phone': sp.provider.phone,
                    'chat_room_id': sp.chat_room_id,
                    'status': sp.status,
                    'created_at': sp.created_at
                })
            
            # Get all chat rooms for this statement
            if hasattr(statement, 'chat_rooms'):
                for chat in statement.chat_rooms.all():
                    debug_info['chat_rooms'].append({
                        'id': chat.id,
                        'initiator_phone': chat.initiator.phone if chat.initiator else None,
                        'receiver_phone': chat.receiver.phone if chat.receiver else None,
                        'status': chat.status,
                        'created_at': chat.created_at
                    })
            
            # Check if current user has responded
            user_response = StatementProvider.objects.filter(statement=statement, provider=request.user).first()
            debug_info['user_has_responded'] = user_response is not None
            if user_response:
                debug_info['user_response'] = {
                    'id': user_response.id,
                    'chat_room_id': user_response.chat_room_id,
                    'status': user_response.status,
                    'created_at': user_response.created_at
                }
            
            return Response(debug_info)
            
        except Statement.DoesNotExist:
            return Response(
                {'error': 'Statement not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(
        detail=False,
        methods=['post'],
        url_path='cleanup-broken-responses'
    )
    def cleanup_broken_responses(self, request):
        """Cleanup endpoint to fix broken StatementProvider records"""
        try:
            # Find StatementProvider records without chat_room_id
            broken_responses = StatementProvider.objects.filter(chat_room_id__isnull=True)
            
            cleanup_info = {
                'total_broken': broken_responses.count(),
                'fixed': 0,
                'failed': 0,
                'details': []
            }
            
            for sp in broken_responses:
                try:
                    # Try to create chat room for this response
                    chat_room_id = create_statement_chat_room(
                        phone_1=sp.statement.author.phone,
                        phone_2=sp.provider.phone,
                        categories=list(sp.statement.categories.values_list('id', flat=True)),
                        location=sp.statement.location,
                        author_name=sp.statement.author.first_name or sp.statement.author.phone,
                        provider_name=sp.provider.first_name or sp.provider.phone,
                        statement_provider_id=sp.id,
                        statement_id=sp.statement.id
                    )
                    
                    if chat_room_id:
                        sp.chat_room_id = chat_room_id
                        sp.save()
                        cleanup_info['fixed'] += 1
                        cleanup_info['details'].append({
                            'statement_provider_id': sp.id,
                            'chat_room_id': chat_room_id,
                            'status': 'fixed'
                        })
                    else:
                        cleanup_info['failed'] += 1
                        cleanup_info['details'].append({
                            'statement_provider_id': sp.id,
                            'status': 'failed - no chat room id returned'
                        })
                        
                except Exception as e:
                    cleanup_info['failed'] += 1
                    cleanup_info['details'].append({
                        'statement_provider_id': sp.id,
                        'status': f'failed - {str(e)}'
                    })
            
            return Response(cleanup_info)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
