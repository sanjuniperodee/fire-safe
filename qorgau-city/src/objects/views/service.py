from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from sms_gateway.mobizon.mobizon_api import MobizonApi

from objects.models import (
    Document,
)


class SmsGetBalanceViewSet(views.APIView):
    permission_classes = [AllowAny, ]
    queryset = Document.objects.prefetch_related('keys').all()

    def get(self, request, *args, **kwargs):
        mobizon_api = MobizonApi()
        response = mobizon_api.get_balance()
        response_data = {}
        if response['code'] == 0:
            response_data = {
                "message": "OK",
                "balance": response['data']['balance'],
                "currency": response['data']['currency'],
            }

        return Response(response_data, status=status.HTTP_200_OK)
