from rest_framework import serializers
from statements.models import StatementRequestForCompleted, StatementProvider
from statements import StatementStatus

class StatementRequestForCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatementRequestForCompleted
        fields = ['id', 'statement', 'provider', 'is_completed']
        #read_only_fields = ['id', 'statement', 'provider']

    def validate(self, data):
        request = self.context.get('request')
        user = request.user

        if not user.is_provider:
            raise serializers.ValidationError({"error": "Only providers can request completion."})

        statement_provider = StatementProvider.objects.filter(
            statement=self.instance.statement,
            provider=user,
            status=StatementStatus.IN_WORK
        ).first()

        if not statement_provider:
            raise serializers.ValidationError({"error": "You must be working on this statement to request completion."})

        return data

    def update(self, instance, validated_data):
        instance.is_completed = validated_data.get('is_completed', instance.is_completed)
        instance.save()

        if instance.is_completed:
            statement_provider = StatementProvider.objects.get(
                statement=instance.statement,
                provider=instance.provider
            )
            statement_provider.status = StatementStatus.COMPLETED
            statement_provider.save()

        return instance