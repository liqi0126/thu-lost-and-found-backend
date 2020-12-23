from django.utils.dateparse import parse_datetime
from rest_framework.test import APITestCase
from rest_framework import status

from .models import User


from rest_framework_simplejwt.tokens import RefreshToken


# Create your tests here.
class UserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', email='js@js.com', password='js.sj', is_superuser=True)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_get_me(self):
        response = self.client.get('/api/v1/users/me/')
        self.assertEqual(response.json()['username'], 'john')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_simple_info(self):
        response = self.client.get(f'/api/v1/users/{self.user.pk}/simple-info/')
        self.assertEqual(response.json()['username'], 'john')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_high_matching_entry(self):
        response = self.client.get(f'/api/v1/users/{self.user.pk}/get-high-matching-entry/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_statistic(self):
        response = self.client.get('/api/v1/users/statistic/')
        self.assertIn('total', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
