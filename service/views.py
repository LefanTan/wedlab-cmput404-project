import uuid
from django.http import QueryDict
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from service.serializers import AuthorSerializer, PostSerializer
from .models import Author, Post


def signup(request):
    if request.method == 'POST':
        body = QueryDict(request.body.decode("utf-8"))

        try:
            # If succeed, author already succeed
            Author.objects.get(displayName=body['username'])
            return render(request, status=status.HTTP_400_BAD_REQUEST, template_name='registration/signup.html', context={"error": "Author already exist!"})
        except Author.DoesNotExist:
            pass

        try:
            # Create user object
            user = User.objects.create_user(
                body['username'], password=body['password'])
            user.save()
        except Exception as e:
            return render(request, status=status.HTTP_400_BAD_REQUEST, template_name='registration/signup.html', context={"error": e})

        try:
            # Create Author object
            author = Author.objects.create(
                uuid=uuid.uuid4().hex,
                user=user,
                displayName=body['username'],
                host=request.build_absolute_uri('/'),
                github=body['github']
            )
            author.profileImage = body['profileImage']
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

        # Add author type to data
        newList = []
        for author in serializer.data:
            newDict = {"type": "author"}
            newDict.update(author)
            newDict['id'] = newDict['url']
            newList.append(newDict)

        return Response({"type": "authors", "items": newList})


@api_view(['GET'])
def author_detail(request, pk):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        newDict = {"type": "author"}
        newDict.update(serializer.data)
        newDict['id'] = newDict['url']

        return Response(newDict)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
# These decorators will cause the entire view to require authentication
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
def posts(request, author_pk, post_pk):
    if request.method == 'GET':
        try:
            author = Author.objects.get(pk=author_pk)
            post = Post.objects.get(pk=post_pk)

            return Response("success")
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
                post = Post.objects.create(
                    id=post_pk,
                    author=author
                )
                postData = PostSerializer(post).data
                return Response(postData)
