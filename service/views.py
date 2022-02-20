from django.conf import settings
from django.http import QueryDict
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User

from service.serializers import AuthorSerializer
from .models import Author, Post

# Create your views here


def signup(request):
    if request.method == 'POST':
        body = QueryDict(request.body.decode("utf-8"))

        try:
            # Create user object and Author object
            user = User.objects.create_user(
                body['username'], password=body['password'])
            user.save()

            author = Author.objects.create(
                displayName=body['username'],
                host=request.build_absolute_uri('/'),
                github=body['github']
            )
            author.profileImage = body['profileImage']
            author.url = f"{author.host}{author.id}"
            author.save()

        except Exception as e:
            return render(request, 'registration/signup.html', {"error": e})

        return redirect('login')
    if request.method == 'GET':
        return render(request, 'registration/signup.html')


@ api_view(['GET'])
def author_list(request):
    if request.method == 'GET':
        author_list = Author.objects.all()
        serializer = AuthorSerializer(author_list, many=True)
        return Response(serializer.data)


@ api_view(['GET'])
def author_detail(request, pk):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        return Response(serializer.data)


@ api_view(['GET', 'POST', 'PUT', 'DELETE'])
def posts(request, author_pk, post_pk):

    if request.method == 'GET':
        try:
            author = Author.objects.get(pk=author_pk)
            post = Post.objects.get(pk=post_pk)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
