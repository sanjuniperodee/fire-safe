from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from auths.models import CustomUser, UserRole, CustomUserRole
import auths


class RegistrationProcessTests(APITestCase):
    """ auths app integration(process) tests for registration process """
    def setUp(self):
        # Create roles from Role in auths.__init__. in CustomUserRole model
        for role in auths.Role.choices:
            CustomUserRole.objects.get_or_create(role=role[0])

        # Setup endpoints for tests
        self.register_url = reverse('auth_register')
        self.login_url = reverse('token_obtain_pair')
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

    def test_full_registration_process(self):
        # Step 1: Register a new user
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Step 2: Check if the user was created in the database
        user = CustomUser.objects.get(phone='+77001234567')
        self.assertIsNotNone(user)

        # Step 3: Check if the user roles were created correctly
        user_roles = UserRole.objects.filter(user=user)
        self.assertEqual(user_roles.count(), 1)
        self.assertEqual(user_roles[0].role.role, 'CITIZEN')

        # Step 4: Try to login with the new user
        login_data = {
            'phone': '+77001234567',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Step 5: Use the access token to make an authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], '+77001234567')
