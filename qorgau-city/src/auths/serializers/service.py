from rest_framework import serializers
from auths.models import CustomUser


class PhoneSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = (
            'phone',
        )


class VerifySmsCodeSerializer(serializers.Serializer):
    code = serializers.CharField()
    phone = serializers.CharField()