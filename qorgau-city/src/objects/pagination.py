from rest_framework.pagination import LimitOffsetPagination as LOPagination
from rest_framework.response import Response


class LimitOffsetPagination(LOPagination):
    def get_paginated_response(self, data):
        return Response({
            'count': self.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'limit': self.limit,
            'offset': self.offset,
            'results': data
        })
