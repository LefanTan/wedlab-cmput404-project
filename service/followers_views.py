import uuid
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema

from service.serializers import AuthorSerializer
from .models import Author, FollowRequest


@swagger_auto_schema(method='get', operation_description="Get a list of followers")
@api_view(['GET'])
def follower_list(request, author_pk):
    try:
        author = Author.objects.get(pk=author_pk)
    except Author.DoesNotExist:
        return Response("Author doens't exist", status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        follow_list = FollowRequest.objects.all().get(actor=author.id)

        page_number = request.GET.get('page')
        size = request.GET.get('size')

        if page_number and size:
            paginator = Paginator(follow_list, size)
            follow_list = paginator.get_page(page_number).object_list
        data = AuthorSerializer(follow_list, many=True).data

        return Response({"type": "followers", "items": data})


@swagger_auto_schema(method='get', operation_description="Get the detail of the current follower")
@swagger_auto_schema(method='put', operation_description="Add the current author as the follower")
@swagger_auto_schema(method='delete', operation_description="Remove the current follower")
@api_view(['GET'])
@api_view(['PUT'])
@api_view(['DELETE'])
def follower_detail(request, author_pk, foreign_author_pk):
    try:
        current = Author.objects.get(pk=author_pk)
        foreign = Author.objects.get(pk=foreign_author_pk)
    except Author.DoesNotExist:
        return Response("Author doens't exist", status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuthorSerializer(foreign)
        return Response(serializer.data)

    if request.method == 'DELETE':
        pass

    if request.method == 'PUT':
        pass