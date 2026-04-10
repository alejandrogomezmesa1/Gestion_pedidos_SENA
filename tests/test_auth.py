from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

class AuthTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
