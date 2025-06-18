from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from auths.models import CustomUser, Education, Experience, Achievement, OtherAchievement
import auths


class ProfileProcessTests(TestCase):
    """ auths app integration(process) tests for provider profile """
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='testprovider',
            email='provider@example.com',
            password='testpass123',
            role=auths.Role.PROVIDER
        )
        self.client.force_authenticate(user=self.user)

    def test_complete_profile_process(self):
        # Step 1: Add Education
        education_data = {
            'college_name': 'Test University',
            'year_start': 2015,
            'year_end': 2019,
            'degree': Education.Degree.BACHELOR
        }
        response = self.client.post(reverse('education-list'), education_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        education_id = response.data['id']

        # Step 2: Add Experience
        experience_data = {
            'company_name': 'Test Company',
            'year_start': 2019,
            'year_end': 2022
        }
        response = self.client.post(reverse('experience-list'), experience_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        experience_id = response.data['id']

        # Step 3: Add Achievement
        achievement_data = {
            'certificate_name': 'Test Certificate',
            'year_received': 2020
        }
        response = self.client.post(reverse('achievement-list'), achievement_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        achievement_id = response.data['id']

        # Step 4: Add Other Achievement
        other_achievement_data = {
            'name': 'Test Other Achievement',
            'year_start': 2018,
            'year_end': 2021
        }
        response = self.client.post(reverse('other-achievement-list'), other_achievement_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        other_achievement_id = response.data['id']

        # Step 5: Verify all profile components
        response = self.client.get(reverse('education-list'))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], education_id)

        response = self.client.get(reverse('experience-list'))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], experience_id)

        response = self.client.get(reverse('achievement-list'))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], achievement_id)

        response = self.client.get(reverse('other-achievement-list'))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], other_achievement_id)

    def test_update_profile_component(self):
        # Create an education entry
        education = Education.objects.create(
            user=self.user,
            college_name='Old University',
            year_start=2010,
            year_end=2014,
            degree=Education.Degree.BACHELOR
        )

        # Update the education entry
        update_data = {
            'college_name': 'New University',
            'year_start': 2011,
            'year_end': 2015,
            'degree': Education.Degree.MASTERS
        }
        response = self.client.put(reverse('education-detail', kwargs={'pk': education.id}), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['college_name'], 'New University')
        self.assertEqual(response.data['degree'], Education.Degree.MASTERS)

    def test_delete_profile_component(self):
        # Create an experience entry
        experience = Experience.objects.create(
            user=self.user,
            company_name='Test Company',
            year_start=2015,
            year_end=2018
        )

        # Delete the experience entry
        response = self.client.delete(reverse('experience-detail', kwargs={'pk': experience.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the experience entry is deleted
        response = self.client.get(reverse('experience-list'))
        self.assertEqual(len(response.data), 0)
