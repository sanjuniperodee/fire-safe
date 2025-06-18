from rest_framework.test import APITestCase

from auths.serializers import UserRegisterSerializer
from auths.models import CustomUser


class UserRegisterSerializerTests(APITestCase):
    """ auths app unit tests for serializers """
    def setUp(self):
        self.valid_payload = {
            'phone': '+77001234567',
            'password': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'middle_name': 'Smith',
            'birthdate': '1990-01-01',
            'role': 'CITIZEN',
            'iin': '123456789012',
        }

    def test_valid_data(self):
        serializer = UserRegisterSerializer(data=self.valid_payload)
        self.assertTrue(serializer.is_valid())

    def test_invalid_role(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['role'] = 'INVALID_ROLE'
        serializer = UserRegisterSerializer(data=invalid_payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn('role', serializer.errors)

    def test_duplicate_phone(self):
        CustomUser.objects.create(phone='+77001234567', email='existing@example.com')
        serializer = UserRegisterSerializer(data=self.valid_payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn('phone', serializer.errors)