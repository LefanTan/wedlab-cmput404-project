from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from service.serializers import AuthorSerializer
from .models import Author, Post

# Create your views here.


@api_view(['GET'])
def author_list(request):
    if request.method == 'GET':
        author_list = Author.objects.all()
        serializer = AuthorSerializer(author_list, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def author_detail(request, pk):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        return Response(serializer.data)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def posts(request, author_pk, post_pk):

    if request.method == 'GET':
        try:
            author = Author.objects.get(pk=author_pk)
            post = Post.objects.get(pk=post_pk)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
