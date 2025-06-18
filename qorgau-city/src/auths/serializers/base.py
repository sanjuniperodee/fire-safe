from rest_framework import serializers
from auths.models import CustomUser


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'phone',
            'last_name',
            'first_name',
            'middle_name',
            'iin',
            'email'
        )