from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from statements.models import StatementRequestForCompleted, StatementProvider
from statements import StatementStatus
from statements.serializers import StatementRequestForCompletedSerializer


class StatementRequestForCompletedViewSet(viewsets.ModelViewSet):
    queryset = StatementRequestForCompleted.objects.all()
    serializer_class = StatementRequestForCompletedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StatementRequestForCompleted.objects.filter(provider=self.request.user)

    @action(detail=True, methods=['post'])
    def set_completed(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={'is_completed': True}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['post'])
    def cancel_request(self, request, pk=None):
        instance = self.get_object()

        # Check if the request belongs to the current user
        # Object Owner can cancel request that belongs to provider
        # if instance.provider != request.user:
        #     return Response({"error": "You can only cancel your own requests."},
        #                     status=status.HTTP_403_FORBIDDEN)

        # Check if the request is not already completed
        if instance.is_completed:
            return Response({"error": "Cannot cancel a completed request."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Delete the request
        instance.delete()

        return Response({"message": "Request cancelled successfully."},
                        status=status.HTTP_204_NO_CONTENT)


    def create(self, request, *args, **kwargs):
        statement_id = request.data.get('statement')

        if not statement_id:
            return Response({"error": "Statement ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # statement_provider = StatementProvider.objects.filter(
        #     statement_id=statement_id,
        #     provider=request.user,
        #     status=StatementStatus.IN_WORK
        # ).first()

        # if not statement_provider:
        #     return Response({"error": "You must be working on this statement to request completion."},
        #                     status=status.HTTP_400_BAD_REQUEST)

        request_for_completed, created = StatementRequestForCompleted.objects.get_or_create(
            statement_id=statement_id,
            provider=request.user,
            defaults={'is_completed': False}
        )

        serializer = self.get_serializer(request_for_completed)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)