from rest_framework import serializers

from objects.models import (
    EvacAddress,
)


class EvacAddressSerializer(serializers.ModelSerializer):
    qrcode_url = serializers.HiddenField(default="")

    class Meta:
        model = EvacAddress
        fields = (
            "id",
            "address",
            "file_path",
            "qrcode_url"
        )


class EvacAddressListSerializer(serializers.ModelSerializer):
    file_path = serializers.CharField()

    class Meta:
        model = EvacAddress
        fields = (
            "id",
            "address",
            "file_path",
            "qrcode_url"
        )
