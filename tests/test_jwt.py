from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

class JWTProtectedTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jwtuser', password='jwtpass')
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'jwtuser', 'password': 'jwtpass'})
        self.token = response.data['access']

    def test_protected_route(self):
        url = reverse('user-list')  # Cambia por una ruta protegida real
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
