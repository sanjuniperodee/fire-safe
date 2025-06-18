import inspect
import json
import os

import auths
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import get_resolver
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from auths.models import CustomUserRole, CustomUser, UserRole

# Before testing do not forget to turn off message sending in auths.models.py file!!!!!!!
# # python manage.py test test
User = get_user_model()


class StatusChecker(APITestCase):
    def setUp(self):
        self.register_url = reverse('auth_register')
        self.login_url = reverse('token_obtain_pair')

        self.client = APIClient(SERVER_NAME='localhost')
        self.test_data_path = os.path.join(os.path.dirname(__file__), 'test_input_output.json')
        with open(self.test_data_path) as f:
            self.test_data = json.load(f)

        # phone and password are used to get fresh access token
        self.phone = "+46221132"
        self.password = "12345Aa@"

        self.user_role = None
        for role in auths.Role.choices:
            new_role = CustomUserRole.objects.get_or_create(role=role[0])
            self.user_role = new_role if role[0] == 'INSPECTOR' else self.user_role

        self.user = CustomUser.objects.create(
            phone=self.phone,
            password=make_password(self.password),
            is_superuser=False,
            is_active=True,
            is_staff=False,
            first_name='Datlas',
            email='user@gmail.com',
            iin="176856098557",
            # status=auths.Status.NOT_ACCEPTED,
        )
        self.user.save()

        self.user_role = UserRole(user=self.user, role=self.user_role[0], status=auths.Status.ACCEPTED)
        self.user_role.save()

        self.user_for_delete = CustomUser.objects.create(
            phone=self.phone + "87",
            password=make_password(self.password),
            is_superuser=False,
            is_active=True,
            is_staff=False,
            first_name='Datlas',
            email='user1@gmail.com',
            iin="17685609857",
            # status=auths.Status.NOT_ACCEPTED,
        )
        self.user_for_delete.save()

    def _get_fresh_access_token(self):
        """Helper function to get a fresh access token"""
        current_method_name = inspect.currentframe().f_code.co_name
        test_case = self.test_data[current_method_name]
        response = self.client.post(self.login_url, test_case['input'], format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f"Failed to obtain token. Response: {response.data}")
        return (response.data['access'],
                response.data['refresh'])

    def _print_url_patterns(self):
        """Helper function to show all url patterns to related urls"""
        resolver = get_resolver()
        for key, value in resolver.reverse_dict.items():
            if isinstance(key, str):
                print(f"{key}: {value[0][0][0]}")

    # Tests start here...
    def test_user_exists_and_active(self):
        """
        Checks if a user exists and is active.
        This is helper checker. Not actual checker.
        """
        user = User.objects.filter(phone=self.phone).first()
        self.assertIsNotNone(user, "User does not exist")
        self.assertTrue(user.is_active, "User is not active")

    def test_register_user(self):
        """
        http://localhost:3000/api/v1/register/
        POST /register/
        """
        current_method_name = inspect.currentframe().f_code.co_name
        # self._print_url_patterns()
        test_case = self.test_data[current_method_name]
        response = self.client.post(self.register_url, test_case['input'], format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(phone=test_case['input']['phone']).exists())

    def test_login_user(self):
        """
        http://localhost:3000/api/v1/login/
        POST /login/
        """
        current_method_name = inspect.currentframe().f_code.co_name
        # self._print_url_patterns()
        test_case = self.test_data[current_method_name]
        response = self.client.post(self.login_url, test_case['input'], format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_refresh_token(self):
        """
        http://localhost:3000/api/v1/login/refresh/
        POST /login/refresh/
        """
        current_method_name = inspect.currentframe().f_code.co_name
        access_token, refresh_token = self._get_fresh_access_token()
        # self._print_url_patterns()

        # Use the access token for an authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.token_refresh = reverse('token_refresh')
        test_case = self.test_data[current_method_name]
        test_case['input']['refresh'] = refresh_token
        response = self.client.post(self.token_refresh, test_case['input'], format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_me(self):
        """
        http://localhost:3000/api/v1/user/me/
        GET /user/me/
        """
        access_token, _ = self._get_fresh_access_token()
        # self._print_url_patterns()

        # Use the access token for an authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.user_me = reverse('user_me-me')
        response = self.client.get(self.user_me)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users(self):
        """
        http://localhost:3000/api/v1/users/
        GET /users/
        """
        access_token, _ = self._get_fresh_access_token()
        # self._print_url_patterns()

        # Use the access token for an authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.user_me = reverse('owners-list')
        response = self.client.get(self.user_me)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_create_users(self):
        """
        http://localhost:3000/api/v1/users/
        POST /users/
        """
        current_method_name = inspect.currentframe().f_code.co_name
        access_token, _ = self._get_fresh_access_token()
        # self._print_url_patterns()

        # Use the access token for an authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.create_user_url = reverse('owners-list')
        test_case = self.test_data[current_method_name]
        response = self.client.post(self.create_user_url, test_case["input"], format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_not_accepted_users(self):
        """
        http://localhost:3000/api/v1/users/not_accepted_users/
        POST /users/not_accepted_users
        """
        access_token, _ = self._get_fresh_access_token()
        # self._print_url_patterns()

        # Use the access token for an authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.not_accepted_users_url = reverse('owners-not-accepted-users')
        response = self.client.get(self.not_accepted_users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users_id(self):
        """
        http://localhost:3000/api/v1/users/1/
        GET /users/{id}/
        """
        access_token, _ = self._get_fresh_access_token()
        # self._print_url_patterns()

        # Use the access token for an authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.users_id = reverse('owners-detail', kwargs={'pk': self.user.id})
        response = self.client.get(self.users_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_patch_users_id(self):
        """
        http://localhost:3000/api/v1/users/1/
        PUT /users/{id}/
        """
        current_method_name = inspect.currentframe().f_code.co_name
        access_token, _ = self._get_fresh_access_token()
        # self._print_url_patterns()

        # Use the access token for an authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.owners_detail = reverse('owners-detail', kwargs={'pk': self.user.id})
        test_case = self.test_data[current_method_name]
        test_case["input"]["id"] = self.user.id
        response = self.client.put(self.owners_detail, data=test_case["input"], format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.patch(self.owners_detail, data=test_case["input"], format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_delete_id(self):
        """
        http://localhost:3000/api/v1/users/1/
        PUT /users/{id}/
        """
        access_token, _ = self._get_fresh_access_token()
        # self._print_url_patterns()

        # Use the access token for an authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.owners_detail = reverse('owners-detail', kwargs={'pk': self.user_for_delete.id})
        response = self.client.delete(self.owners_detail, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class InputOutputChecker(APITestCase):
    def setUp(self):
        self.register_url = reverse('auth_register')
        self.login_url = reverse('token_obtain_pair')

        self.client = APIClient(SERVER_NAME='localhost')
        self.test_data_path = os.path.join(os.path.dirname(__file__), 'test_input_output.json')
        with open(self.test_data_path) as f:
            self.test_data = json.load(f)

        # phone and password are used to get fresh access token
        self.phone = "+46221132"
        self.password = "12345Aa@"

        self.user_role = None
        for role in auths.Role.choices:
            new_role = CustomUserRole.objects.get_or_create(role=role[0])
            self.user_role = new_role if role[0] == 'INSPECTOR' else self.user_role

        self.user = CustomUser.objects.create(
            phone=self.phone,
            password=make_password(self.password),
            is_superuser=False,
            is_active=True,
            is_staff=False,
            first_name='Datlas',
            email='user@gmail.com',
            iin="176856098557",
            # status=auths.Status.NOT_ACCEPTED,
        )
        self.user.save()

        self.user_role = UserRole(user=self.user, role=self.user_role[0], status=auths.Status.ACCEPTED)
        self.user_role.save()

        self.user_for_delete = CustomUser.objects.create(
            phone=self.phone + "87",
            password=make_password(self.password),
            is_superuser=False,
            is_active=True,
            is_staff=False,
            first_name='Datlas',
            email='user1@gmail.com',
            iin="17685609857",
            # status=auths.Status.NOT_ACCEPTED,
        )
        self.user_for_delete.save()

    def _get_fresh_access_token(self):
        """Helper function to get a fresh access token"""
        data = {
            "phone": self.phone,
            "password": self.password
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f"Failed to obtain token. Response: {response.data}")
        return response.data['access'], response.data['refresh']

    def _print_url_patterns(self):
        """Helper function to show all url patterns to related urls"""
        resolver = get_resolver()
        for key, value in resolver.reverse_dict.items():
            if isinstance(key, str):
                print(f"{key}: {value[0][0][0]}")

    def test_register_user(self):
        """
        http://localhost:3000/api/v1/register/
        POST /register/
        """
        current_method_name = inspect.currentframe().f_code.co_name
        test_case = self.test_data[current_method_name]
        response = self.client.post(self.register_url, test_case['input'], format='json')

        expected_output = self.test_data[current_method_name]["output"]
        response_output = response.data
        # Check each field in the response
        for key, expected_value in expected_output.items():
            if key == 'role':
                # Special handling for the 'role' field
                self.assertEqual(len(response_output[key]), len(expected_value))
                for i, role in enumerate(expected_value):
                    for role_key, role_value in role.items():
                        self.assertEqual(response_output[key][i][role_key], role_value)
            else:
                self.assertEqual(response_output[key], expected_value,
                                 f"Mismatch in field '{key}': expected {expected_value}, got {response_output[key]}")

    def test_user_me(self):
        """
        http://localhost:3000/api/v1/user/me/
        GET /user/me/
        """
        current_method_name = inspect.currentframe().f_code.co_name
        access_token, _ = self._get_fresh_access_token()

        # Use the access token for an authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.user_me = reverse('user_me-me')

        response = self.client.get(self.user_me)

        expected_output = self.test_data[current_method_name]["output"]
        response_output = response.data
        # Check each field in the response
        for key, expected_value in expected_output.items():
            if key == 'role':
                # Special handling for the 'role' field
                self.assertEqual(len(response_output[key]), len(expected_value))
                for i, role in enumerate(expected_value):
                    for role_key, role_value in role.items():
                        self.assertEqual(response_output[key][i][role_key], role_value)
            else:
                self.assertEqual(response_output[key], expected_value,
                                 f"Mismatch in field '{key}': expected {expected_value}, got {response_output[key]}")

    def test_get_users(self):
        """
        http://localhost:3000/api/v1/users/
        GET /users/
        """
        current_method_name = inspect.currentframe().f_code.co_name
        access_token, _ = self._get_fresh_access_token()

        # Use the access token for an authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.user_me = reverse('owners-list')

        response = self.client.get(self.user_me)
        expected_outputs = self.test_data[current_method_name]["output"]
        response_output = response.data
        for i, user in enumerate(response_output):
            expected_user = response_output[i]
            expected_output = expected_outputs[i]
            # Check each field in the response
            for key, expected_value in expected_output.items():
                if key == 'role':
                    for i, role in enumerate(expected_value):
                        for role_key, role_value in role.items():
                            self.assertEqual(expected_user[key][0][role_key], role_value)
                else:
                    self.assertEqual(expected_user[key], expected_value,
                                     f"Mismatch in field '{key}': expected {expected_value}, got {expected_user[key]}")

    def test_partial_create_users(self):
        """
        http://localhost:3000/api/v1/users/
        POST /users/
        """
        current_method_name = inspect.currentframe().f_code.co_name
        access_token, _ = self._get_fresh_access_token()
        # self._print_url_patterns()

        # Use the access token for an authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.create_user_url = reverse('owners-list')

        test_case = self.test_data[current_method_name]
        response = self.client.post(self.create_user_url, test_case["input"], format='multipart')
        expected_output = self.test_data[current_method_name]["output"]
        response_output = response.data
        # Check each field in the response
        for key, expected_value in expected_output.items():
            self.assertEqual(response_output[key], expected_value,
                             f"Mismatch in field '{key}': expected {expected_value}, got {response_output[key]}")

    def test_not_accepted_users(self):
        """
        http://localhost:3000/api/v1/users/not_accepted_users/
        POST /users/not_accepted_users
        """
        current_method_name = inspect.currentframe().f_code.co_name
        access_token, _ = self._get_fresh_access_token()
        # self._print_url_patterns()

        # Use the access token for an authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.not_accepted_users_url = reverse('owners-not-accepted-users')

        response = self.client.get(self.not_accepted_users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_outputs = self.test_data[current_method_name]["output"]
        response_output = response.data
        if response_output:
            for i, user in enumerate(response_output):
                expected_user = response_output[i]
                expected_output = expected_outputs[i]
                # Check each field in the response
                for key, expected_value in expected_output.items():
                    if key == 'role':
                        for i, role in enumerate(expected_value):
                            for role_key, role_value in role.items():
                                self.assertEqual(expected_user[key][0][role_key], role_value)
                    else:
                        self.assertEqual(expected_user[key], expected_value,
                                         f"Mismatch in field '{key}': expected {expected_value}, got {expected_user[key]}")
        # If output is empty: []
        else:
            self.assertEqual(response_output, expected_outputs)

    def test_get_users_id(self):
        """
        http://localhost:3000/api/v1/users/1/
        GET /users/{id}/
        """
        current_method_name = inspect.currentframe().f_code.co_name
        access_token, _ = self._get_fresh_access_token()
        # self._print_url_patterns()

        # Use the access token for an authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.users_id = reverse('owners-detail', kwargs={'pk': self.user.id})

        response = self.client.get(self.users_id)
        expected_output = self.test_data[current_method_name]["output"]
        response_output = response.data
        # Check each field in the response
        for key, expected_value in expected_output.items():
            if key == 'role':
                # Special handling for the 'role' field
                self.assertEqual(len(response_output[key]), len(expected_value))
                for i, role in enumerate(expected_value):
                    for role_key, role_value in role.items():
                        self.assertEqual(response_output[key][i][role_key], role_value)
            else:
                self.assertEqual(response_output[key], expected_value,
                                 f"Mismatch in field '{key}': expected {expected_value}, got {response_output[key]}")

    def test_put_patch_users_id(self):
        """
        http://localhost:3000/api/v1/users/1/
        PUT /users/{id}/
        """
        current_method_name = inspect.currentframe().f_code.co_name
        access_token, _ = self._get_fresh_access_token()
        # self._print_url_patterns()

        # Use the access token for an authenticated request
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.owners_detail = reverse('owners-detail', kwargs={'pk': self.user.id})

        test_case = self.test_data[current_method_name]
        test_case["input"]["id"] = self.user.id

        # PATCH method checking
        response = self.client.patch(self.owners_detail, data=test_case["input"], format='multipart')
        expected_output = self.test_data[current_method_name]["output"]
        response_output = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check each field in the response
        for key, expected_value in expected_output.items():
            self.assertEqual(response_output[key], expected_value,
                             f"Mismatch in field '{key}': expected {expected_value}, got {response_output[key]}")
