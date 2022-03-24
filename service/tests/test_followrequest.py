from rest_framework import status
from django.urls import reverse
from service.models import Author, FollowRequest
import urllib
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase


class FollowRequestEndpointsTestCase(APITestCase):
    def setUp(self):
        self.apiClient = APIClient()

        self.apiClient.post(reverse('signup'), data=urllib.parse.urlencode({
            "username": "admin1",
            "password": "root",
            "github": "https://link.com"
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")
        self.apiClient.post(reverse('signup'), data=urllib.parse.urlencode({
            "username": "admin2",
            "password": "root",
            "github": "https://link.com"
        }), SERVER_NAME="test.com", content_type="application/x-www-form-urlencoded")

        self.apiClient.login(username="admin1", password="root")

        self.sender = Author.objects.get(displayName="admin1")
        self.receiver = Author.objects.get(displayName="admin2")

        self.followrequest = FollowRequest.objects.create(
            summary=f"{self.sender.displayName} wants to follow {self.receiver.displayName}",
            actor=self.sender,
            object=self.receiver.id
        )
        self.follow_info = {
            "id": self.followrequest.id,
            "type": "Follow"
        }

    # Test send request
    def test_send_follow_request(self):
        params = {"author_pk": self.sender.id}
        data = {
            'id': '1',
            'summary': f"{self.sender.displayName} wants to follow {self.receiver.displayName}",
            'type': 'Follow',
            'actor': self.sender.id,
            'object': self.receiver
        }
        response = self.apiClient.post(reverse('follow_request', kwargs=params), data=self.follow_info,
                                       format='json', SERVER_NAME="test.com")

        request = FollowRequest.objects.get(actor=self.sender.id)

        self.assertEqual(request.actor.id, self.sender.id)
        self.assertEqual(request.object, self.receiver.id)


