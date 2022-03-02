import uuid

from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_yasg.utils import swagger_auto_schema

from service.serializers import FollowRequestSerializer
from .models import Author, FollowRequest


@swagger_auto_schema(method='get', auto_schema=None)
@swagger_auto_schema(method='post', operation_description="send a follow request to another person")
@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def send_request(request):
    # Send the friend request
    if request.method == 'GET':
        return render(request, 'add_friends_form.html')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response("Authentication required", status=status.HTTP_401_UNAUTHORIZED)
        else:
            body = request.data
            print(body.get('displayName'))

            try:
                Author.objects.get(displayName=body.get('displayName'))
                data = {
                    'id': uuid.uuid4().hex,
                    'summary': f"{Author.objects.get('displayName')} wants to follow {body.get('displayName')}",
                    'actor': Author.objects.filter(displayName=Author.objects.get('displayName')),
                    'object': Author.objects.filter(displayName=body.get('displayName'))
                }

                follow_serializer = FollowRequestSerializer(data=data)

                if follow_serializer.is_valid():
                    follow_serializer.save()
                    return Response(follow_serializer.data)
                return render(request, status=status.HTTP_400_BAD_REQUEST, template_name='add_friends_form.html',
                              context={"error": follow_serializer.errors})

            except Author.DoesNotExist:
                return render(request, status=status.HTTP_400_BAD_REQUEST, template_name='add_friends_form.html',
                              context={"error": "Author Does Not Exist, Please try again!"})