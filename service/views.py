import json
from tkinter.tix import Form
import uuid
from django.http import QueryDict
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from service.serializers import AuthorSerializer, PostSerializer
from .models import Author, Category, Post


@api_view(['GET', 'POST'])
@parser_classes([FormParser])
def signup(request):
    if request.method == 'POST':
        body = request.data

        try:
            # If succeed, author already succeed
            Author.objects.get(displayName=body.get('username'))
            return render(request, status=status.HTTP_400_BAD_REQUEST, template_name='registration/signup.html', context={"error": "Author already exist!"})
        except Author.DoesNotExist:
            pass

        try:
            # Create user object
            user = User.objects.create_user(
                body.get('username'), password=body.get('password'))
            user.save()
        except Exception as e:
            return render(request, status=status.HTTP_400_BAD_REQUEST, template_name='registration/signup.html', context={"error": e})

        try:
            # Create Author object
            author = Author.objects.create(
                uuid=uuid.uuid4().hex,
                user=user,
                displayName=body.get('username'),
                host=request.build_absolute_uri('/'),
                github=body.get('github')
            )
            author.profileImage = body.get('profileImage')
            author.url = f"{author.host}authors/{author.uuid}"
            author.save()
        except Exception as e:
            user.delete()
            return render(request, status=status.HTTP_400_BAD_REQUEST, template_name='registration/signup.html', context={"error": e})

        return redirect('login')
    if request.method == 'GET':
        return render(request, 'registration/signup.html')


@api_view(['GET'])
def author_list(request):
    if request.method == 'GET':
        author_list = Author.objects.all()
        serializer = AuthorSerializer(author_list, many=True)

        return Response({"type": "authors", "items": serializer.data})


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
@parser_classes([MultiPartParser, FormParser])
# These decorators will cause the entire view to require authentication
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def post_detail(request, author_pk, post_pk):
    if request.method == 'GET':
        try:
            author = Author.objects.get(pk=author_pk)
            post = Post.objects.get(pk=post_pk)

            authorData = AuthorSerializer(author).data
            postData = PostSerializer(post).data

            postData['author'] = authorData

            return Response(postData)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response("Authentication required", status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                author = Author.objects.get(pk=author_pk)
                post = Post.objects.get(pk=post_pk)

                return Response(f"post object of id-{post_pk} already exist, use PUT to update the post object", status=status.HTTP_400_BAD_REQUEST)
            except Author.DoesNotExist:
                return Response(f"Author of id-{author_pk} doesn't exist", status=status.HTTP_404_NOT_FOUND)
            except Post.DoesNotExist:
                # If post doesn't exist, create one
                newDict = create_post(request, author, post_pk)
                return Response(newDict)


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def posts(request, author_pk):
    if request.method == 'GET':
        try:
            author = Author.objects.get(pk=author_pk)
            posts = author.post_set.all()

            postsData = PostSerializer(posts, many=True).data
            newData = []
            for post in postsData:
                newDict = {}
                newDict.update(post)

                # grab associated categories and append
                category_list = []
                for category in Post.objects.get(pk=post.get('id')).categories.all():
                    category_list.append(category.name)
                newDict['categories'] = category_list

                newData.append(newDict)

            return Response(newData)
        except Author.DoesNotExist:
            return Response('Author doesn\'t exist', status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        try:
            author = Author.objects.get(pk=author_pk)
        except Author.DoesNotExist:
            return Response("Author doesn't exist", status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_authenticated or request.user.id != author.user_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                newDict = create_post(request, author)

                return Response(newDict)
            except Author.DoesNotExist:
                return Response('Author doesn\'t exist', status=status.HTTP_404_NOT_FOUND)


def create_post(request, author, id=None):
    post = Post.objects.create(
        id=id,
        uuid=uuid.uuid4().hex,
        author=author,
        title=request.data.get('title'),
        description=request.data.get('description', ''),
    )
    post.url = request.build_absolute_uri('/') + post.uuid

    # Grab category data
    category_list = []
    for category in json.loads(request.data.get('categories').replace('\'', '"')):
        category_obj, created = Category.objects.get_or_create(
            name=category)
        category_list.append(category_obj.name)
        post.categories.add(category_obj)

    post.save()

    postData = PostSerializer(post).data
    newDict = {"categories": category_list}
    newDict.update(postData)

    # Add author data
    authorData = AuthorSerializer(author).data
    newDict['author'] = authorData

    return newDict
