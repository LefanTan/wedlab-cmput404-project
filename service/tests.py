from django.test import TestCase, override_settings
from django.urls import reverse
from django.conf import settings
from .models import Author
import os
import urllib
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APIClient, APITestCase


class AuthEndpointsTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.apiClient = APIClient()

    @override_settings(DEBUG=True)
    def test_create_user(self):
        response = self.apiClient.post(reverse('signup'), data=urllib.parse.urlencode({
            "username": "admin",
            "password": "root",
            "github": "https://link.com"
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")

        print(response.content)
        print(settings.DEBUG)

        success = self.apiClient.login(username="admin", password="root")

        self.assertEqual(response.status_code, 302)
        self.assertTrue(success)
