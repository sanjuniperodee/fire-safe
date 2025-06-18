from django.db.models import Case, When, Value, BooleanField, IntegerField, OuterRef, Subquery
from django_filters import rest_framework as filters

from statements.models import Statement, SeenStatement


class BooleanOrderingFilter(filters.OrderingFilter):
    ordering_param = 'ordering'
    ordering_fields = ['created_at', 'seen', 'seen_at']

    def get_ordering(self, request, queryset, view):
        params = request.query_params.get(self.ordering_param)
        if params:
            fields = [param.strip() for param in params.split(',')]
            ordering = self.remove_invalid_fields(queryset, fields, view, request)
            if ordering:
                return ordering
        return self.get_default_ordering(view)

    def filter_queryset(self, request, queryset, view):
        if 'seen' in request.query_params and request.query_params.get('seen') == 'true':
            seen_subquery = SeenStatement.objects.filter(
                user=request.user,
                statement=OuterRef('pk')
            ).values('seen_at')

            queryset = queryset.annotate(
                is_seen=Case(
                    When(id__in=SeenStatement.objects.filter(user=request.user).values('statement_id'),
                         then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                ),
                custom_order=Case(
                    When(is_seen=True, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField()
                ),
                seen_at=Subquery(seen_subquery)
            )
            return queryset.order_by('custom_order', '-seen_at', '-created_at')
        return queryset

    def remove_invalid_fields(self, queryset, fields, view, request):
        valid_fields = [item[0] for item in self.get_valid_fields(queryset, view, {'request': request})]
        return [term for term in fields if term.lstrip('-') in valid_fields]

    def get_valid_fields(self, queryset, view, context=None):
        valid_fields = getattr(view, 'ordering_fields', self.ordering_fields)
        if valid_fields is None:
            return [
                (field_name, field_name) for field_name in view.get_serializer().fields.keys()
            ]
        elif valid_fields == '__all__':
            valid_fields = [
                (field.name, field.verbose_name) for field in queryset.model._meta.fields
            ]
        else:
            valid_fields = [
                (item, item) if isinstance(item, str) else item
                for item in valid_fields
            ]
        return valid_fields

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': self.ordering_param,
                'required': False,
                'in': 'query',
                'description': 'Which field to use when ordering the results.',
                'schema': {
                    'type': 'string',
                },
            },
        ]


class StatementFilter(filters.FilterSet):
    seen = filters.BooleanFilter(method='filter_seen')
    min_price = filters.NumberFilter(field_name="min_price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="max_price", lookup_expr='lte')
    created_at = filters.DateTimeFromToRangeFilter()
    ordering = BooleanOrderingFilter(
        fields=(
            ('seen', 'seen'),
            ('created_at', 'created_at'),
        )
    )

    class Meta:
        model = Statement
        fields = ['min_price', 'max_price', 'created_at', 'seen']

    def filter_seen(self, queryset, name, value):
        user = self.request.user
        if user.is_provider:
            seen_statements = SeenStatement.objects.filter(user=user).values_list('statement_id', flat=True)

            queryset = queryset.annotate(
                seen=Case(
                    When(id__in=seen_statements, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                )
            )
        return queryset