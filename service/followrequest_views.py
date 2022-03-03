import uuid

from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_yasg.utils import swagger_auto_schema

from service.serializers import FollowRequestSerializer, InboxObject
from .models import Author, FollowRequest


@swagger_auto_schema(method='post', operation_description="send a follow request to another person")
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def send_request(request, author_pk):
    # Send the friend request
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response("Authentication required", status=status.HTTP_401_UNAUTHORIZED)
        else:
            body = request.data

            try:
                author = Author.objects.get(displayName=body.get('displayName'))  # Receiver
                current = Author.objects.get(pk=author_pk)
                data = {
                    'id': uuid.uuid4().hex,
                    'summary': f"{current.displayName} wants to follow {author.displayName}",
                    'type': 'Follow',
                    'actor': current.id,
                    'object': author.id
                }

                follow_serializer = FollowRequestSerializer(data=data)

                if follow_serializer.is_valid():
                    follow_serializer.save()

                    # Send the request data to the receiver's inbox
                    object = FollowRequest.objects.get(pk=data['id'])
                    inbox_item = InboxObject(content_object=object, author=author)
                    inbox_item.save()
                    # , model_to_dict(inbox_item)
                    return Response(follow_serializer.data)
                return Response("Data not valid", status=status.HTTP_400_BAD_REQUEST)
            except Author.DoesNotExist:
                return Response("Username does not exist!", status=status.HTTP_400_BAD_REQUEST)