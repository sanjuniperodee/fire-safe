from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from auths.models import CustomUser, UserRole, CustomUserRole
import auths


class UserRegisterViewTests(APITestCase):
    """ auths app unit tests for views """
    def setUp(self):
        # Create roles from Role in auths.__init__. in CustomUserRole model
        for role in auths.Role.choices:
            CustomUserRole.objects.get_or_create(role=role[0])

        # Setup endpoints for tests
        self.register_url = reverse('auth_register')
        self.user_detail_url = reverse('user_me-me')
        self.valid_payload = {
            "last_name": "Citizen",
            "first_name": "Citizen",
            "middle_name": "Citizen",
            "email": "citizen@example.com",
            "phone": "+77001234567",
            "birthdate": "2024-08-20",
            "role": "CITIZEN",
            "iin": "111666999888",
            "actual_residence_address": "Astana, Turan 65/2",
            "residence_address": "Astana, Kabanbay Batyra 52/2",
            "password": "testpassword123",
            "password2": "testpassword123"
        }

    def test_valid_registration(self):
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(phone='+77001234567').exists())

    def test_invalid_registration(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['email'] = 'invalid_email'
        response = self.client.post(self.register_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_detail(self):
        # First, register a user
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        user_id = response.data['id']
        print('unit test runs')

        # Then, try to get user details
        # detail_url = reverse(self.user_detail_url, kwargs={'pk': user_id})
        # response = self.client.get(detail_url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['phone'], '+77001234567')
