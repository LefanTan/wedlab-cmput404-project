from django.test import TestCase
from django.urls import reverse
from .models import Author
import urllib
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APIClient, APITestCase


class AuthEndpointsTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.apiClient = APIClient()

    def test_create_user(self):
        response = self.apiClient.post(reverse('signup'), data=urllib.parse.urlencode({
            "username": "admin",
            "password": "root",
            "github": "https://link.com"
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")

        print(response.content)

        success = self.apiClient.login(username="admin", password="root")

        self.assertEqual(response.status_code, 302)
        self.assertTrue(success)
