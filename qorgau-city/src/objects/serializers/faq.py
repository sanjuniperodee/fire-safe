from rest_framework import serializers

from objects.models import (
    FAQ,
)


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = (
            'question',
            'answer'
        )
