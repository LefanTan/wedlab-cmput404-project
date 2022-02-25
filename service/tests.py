from rest_framework import status
from django.urls import reverse
from .models import Author
import json
import urllib
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APIClient, APITestCase


def get_dict(byte):
    return json.loads(byte.decode("UTF-8"))


class AuthorEndpointsTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
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


class PostEndpointsTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.apiClient = APIClient()

        self.apiClient.post(reverse('signup'), data=urllib.parse.urlencode({
            "username": "admin",
            "password": "root",
            "github": "https://link.com"
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")
        self.apiClient.login(username="admin", password="root")

        self.author = Author.objects.get(displayName="admin")

    def test_create_post_with_list(self):
        # Create two post
        self.apiClient.post(reverse('post_list', kwargs={"author_pk": self.author.id}), data=urllib.parse.urlencode({
            "title": "title1",
            "description": "description text",
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")
        self.apiClient.post(reverse('post_list', kwargs={"author_pk": self.author.id}), data=urllib.parse.urlencode({
            "title": "title2",
            "description": "description text",
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")

        # query the post by author id
        response = self.apiClient.get(reverse('post_list', kwargs={
            "author_pk": self.author.id}), SERVER_NAME="test.com")

        dict = get_dict(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("title1", dict[0].get('title'))
        self.assertEqual("title2", dict[1].get('title'))
