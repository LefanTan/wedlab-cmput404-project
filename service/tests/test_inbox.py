from rest_framework import status
from service.models import Author, InboxObject, Post
import json
import urllib
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APIClient, APITestCase

def get_dict(byte):
    return json.loads(byte.decode("UTF-8"))

class InboxEndpointsTestCase(APITestCase):

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
        self.post = Post.objects.create(
            author=self.author,
            title="test_title",
            description="description",
            visibility="PUBLIC"
        )
        self.post_info = {
            "id": self.post.id,
            "type": "post"
        }

    #test inbox_list POST and GET
    def test_inbox_list(self):
        response = self.apiClient.post(reverse('inbox_list', kwargs={"pk": self.author.id}), 
        data=self.post_info, format='json',
        SERVER_NAME="test.com")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.apiClient.get(reverse('inbox_list', kwargs={
            "pk": self.author.id}), SERVER_NAME="test.com")
        dict = get_dict(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(dict.get('items')))
