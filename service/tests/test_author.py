from rest_framework import status
from django.urls import reverse
from service.models import Author
import json
import urllib
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase


def get_dict(byte):
    return json.loads(byte.decode("UTF-8"))


class AuthorEndpointsTestCase(APITestCase):
    def setUp(self):
        self.apiClient = APIClient()
        self.default_user = User.objects.create_user(
            username="default_user", password="root")

    # Test signup endpoint and login
    def test_create_user(self):
        response = self.apiClient.post(reverse('signup'), data=urllib.parse.urlencode({
            "username": "admin",
            "password": "root",
            "github": "https://link.com"
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")

        success = self.apiClient.login(username="admin", password="root")

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        try:
            author = Author.objects.get(displayName="admin")
        except Exception as e:
            self.fail('Unable to retrieve author object')

        self.assertTrue(success)
        self.assertEqual(author.displayName, "admin")

    # Test author_list GET
    def test_get_authors(self):
        # User 1
        self.apiClient.post(reverse('signup'), data=urllib.parse.urlencode({
            "username": "user1",
            "password": "root",
            "github": "https://link.com"
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")
        # User 2
        self.apiClient.post(reverse('signup'), data=urllib.parse.urlencode({
            "username": "user2",
            "password": "root",
            "github": "https://link.com"
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")
        # User 3
        self.apiClient.post(reverse('signup'), data=urllib.parse.urlencode({
            "username": "user3",
            "password": "root",
            "github": "https://link.com"
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")

        response = self.apiClient.get(reverse(
            'author_list'), SERVER_NAME="test.com")

        dict = get_dict(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(3, len(dict.get('items')))

    # Test author_detail GET
    def test_get_specific_author(self):
        # User 1
        self.apiClient.post(reverse('signup'), data=urllib.parse.urlencode({
            "username": "user1",
            "password": "root",
            "github": "https://link.com"
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")

        author = Author.objects.get(displayName="user1")

        response = self.apiClient.get(reverse(
            'author_detail', kwargs={"pk": author.id}), SERVER_NAME="test.com")

        dict = get_dict(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict.get('displayName'), "user1")
        self.assertEqual(dict.get('type'), "author")

    # Test author_detail POST / Test update profile
    def test_post_specific_author(self):
        # User 1
        self.apiClient.post(reverse('signup'), data=urllib.parse.urlencode({
            "username": "user1",
            "password": "root",
            "github": "https://link.com"
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")
        author = Author.objects.get(displayName="user1")

        self.apiClient.login(username="user1", password="root")

        response = self.apiClient.post(reverse(
            'author_detail', kwargs={"pk": author.id}), data=urllib.parse.urlencode({
                "displayName": "newusername",
                "github": "https://newlink.com"
            }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Login again with new username
        success = self.apiClient.login(username="newusername", password="root")
        self.assertTrue(success)

        dict = get_dict(response.content)

        self.assertEqual(dict.get('displayName'), "newusername")
        self.assertEqual(dict.get('github'), "https://newlink.com")
