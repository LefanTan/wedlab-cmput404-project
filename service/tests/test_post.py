from rest_framework import status
from django.urls import reverse
from service.models import Author
import urllib
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase

from service.tests.test_author import get_dict


class PostEndpointsTestCase(APITestCase):
    def setUp(self):
        self.apiClient = APIClient()

        self.apiClient.post(reverse('signup'), data=urllib.parse.urlencode({
            "username": "admin",
            "password": "root",
            "github": "https://link.com"
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")
        self.apiClient.login(username="admin", password="root")
        self.author = Author.objects.get(displayName="admin")

    # Test create and get post with post list
    def test_post_list(self):
        # Create two post
        self.apiClient.post(reverse('post_list', kwargs={"author_pk": self.author.id}), data=urllib.parse.urlencode({
            "title": "title1",
            "description": "description text",
            "categories": ["what", "nice"],
            "unlisted": True,
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")
        self.apiClient.post(reverse('post_list', kwargs={"author_pk": self.author.id}), data=urllib.parse.urlencode({
            "title": "title2",
            "description": "description text",
            "categories": [],
            "unlisted": False,
            "visibility": "PUBLIC"
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")

        # query the post by author id
        response = self.apiClient.get(reverse('post_list', kwargs={
            "author_pk": self.author.id}), SERVER_NAME="test.com")

        dict = get_dict(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("title1", dict[0].get('title'))
        self.assertEqual("title2", dict[1].get('title'))

    # Test create and get post with post detail
    def test_create_post_detail(self):
        params = {"author_pk": self.author.id, "post_pk": 1}
        self.apiClient.put(reverse('post_detail', kwargs=params), data=urllib.parse.urlencode({
            "title": "post1",
            "description": "description text",
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")

        # query the post by author id
        response = self.apiClient.get(
            reverse('post_detail', kwargs=params), SERVER_NAME="test.com")

        dict = get_dict(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict.get('id'), "1")
        self.assertEqual(dict.get('author').get('displayName'), "admin")

    # Test update post with post detail
    def test_update_post_detail(self):
        params = {"author_pk": self.author.id, "post_pk": 1}
        self.apiClient.put(reverse('post_detail', kwargs=params), data=urllib.parse.urlencode({
            "title": "post1",
            "description": "description text",
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")

        self.apiClient.post(reverse('post_detail', kwargs=params), data=urllib.parse.urlencode({
            "title": "new name",
            "description": "new description",
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")

        # query the post by author id
        response = self.apiClient.get(
            reverse('post_detail', kwargs=params), SERVER_NAME="test.com")

        dict = get_dict(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict.get('id'), "1")
        self.assertEqual(dict.get('title'), "new name")
        self.assertEqual(dict.get('description'), "new description")

    # Test delete post with post detail
    def test_delete_post_detail(self):
        params = {"author_pk": self.author.id, "post_pk": 1}
        self.apiClient.put(reverse('post_detail', kwargs=params), data=urllib.parse.urlencode({
            "title": "post1",
            "description": "description text",
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")

        # query the post by author id
        response = self.apiClient.get(
            reverse('post_detail', kwargs=params), SERVER_NAME="test.com")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete the post
        delete_response = self.apiClient.delete(
            reverse('post_detail', kwargs=params), SERVER_NAME="test.com")

        # query the post by author id, which shouldn't exist anymore
        get_response = self.apiClient.get(
            reverse('post_detail', kwargs=params), SERVER_NAME="test.com")

        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)
