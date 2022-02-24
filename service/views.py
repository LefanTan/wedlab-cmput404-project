import uuid
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from service.serializers import AuthorSerializer, CategorySerializer, PostSerializer, UserSerializer
from .models import Author, Category, Post


@api_view(['GET', 'POST'])
@parser_classes([FormParser])
def signup(request):
    if request.method == 'POST':
        body = request.data

        try:
            # If succeed, author already exist
            Author.objects.get(displayName=body.get('username'))
            return render(request, status=status.HTTP_400_BAD_REQUEST, template_name='registration/signup.html', context={"error": "Author already exist!"})
        except Author.DoesNotExist:
            pass

        # Create Author object
        cp = body.copy()
        cp['id'] = uuid.uuid4().hex
        cp['host'] = request.build_absolute_uri('/')
        cp['url'] = f"{cp.get('host')}authors/{cp.get('id')}"
        cp['displayName'] = cp['username']

        user_data = {
            "username": body.get('username'),
            "password": body.get('password')
        }
        author_serializer = AuthorSerializer(data=cp)

        if author_serializer.is_valid():
            author_serializer.save(user=user_data)
            return redirect('login')
        return render(request, status=status.HTTP_400_BAD_REQUEST, template_name='registration/signup.html', context={"error": author_serializer.errors})
    if request.method == 'GET':
        return render(request, 'registration/signup.html')


@ api_view(['GET'])
# Return a list of authors
def author_list(request):
    if request.method == 'GET':
        author_list = Author.objects.all()

        page_number = request.GET.get('page')
        size = request.GET.get('size')

        if page_number and size:
            paginator = Paginator(author_list, size)
            author_list = paginator.get_page(page_number).object_list
        data = AuthorSerializer(author_list, many=True).data

        return Response({"type": "authors", "items": data})


@ api_view(['GET', 'POST'])
@ parser_classes([FormParser, MultiPartParser])
# Return a specific author
def author_detail(request, pk):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return Response("Author doens't exist", status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        return Response(serializer.data)
    # Update author
    if request.method == 'POST':
        if not request.user.is_authenticated or request.user.id != author.user_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            password = request.data.get('password')
            username = request.data.get('username')
            if password:
                request.user.set_password(password)

            if username:
                request.user.username = username
                request.user.save()

            serializer = AuthorSerializer(
                author, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET', 'POST', 'PUT', 'DELETE'])
@ parser_classes([MultiPartParser, FormParser])
# These decorators will cause the entire view to require authentication
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])
# Return a specific Post
def post_detail(request, author_pk, post_pk):
    if request.method == 'GET':
        try:
            author = Author.objects.get(pk=author_pk)
            post = author.post_set.get(pk=post_pk)

            postData = PostSerializer(post).data

            return Response(postData)
        except Author.DoesNotExist:
            return Response("Author doesn't exist", status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            return Response("Post doesn't exist", status=status.HTTP_404_NOT_FOUND)
    # Create a post
    if request.method == 'PUT':
        try:
            author = Author.objects.get(pk=author_pk)
            post = author.post_set.get(pk=post_pk)

            return Response(f"Post object of id-{post_pk} already exist, use POST to update the post object", status=status.HTTP_400_BAD_REQUEST)
        except Author.DoesNotExist:
            return Response(f"Author of id-{author_pk} doesn't exist", status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            # If post doesn't exist, create one
            return create_post(request, author, post_pk)
    # Updates a post
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response("Authentication required", status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                author = Author.objects.get(pk=author_pk)
                post = author.post_set.get(pk=post_pk)

                postSerializer = PostSerializer(
                    post, data=request.data, partial=True)
                if postSerializer.is_valid():
                    postSerializer.save()
                    return Response(postSerializer.data)
                return Response(postSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Author.DoesNotExist:
                return Response(f"Author of id-{author_pk} doesn't exist", status=status.HTTP_404_NOT_FOUND)
            except Post.DoesNotExist:
                return Response(f"Author of id-{author_pk} doesn't have this post", status=status.HTTP_404_NOT_FOUND)
    # Deletes a post
    if request.method == 'DELETE':
        try:
            author = Author.objects.get(pk=author_pk)
            post = author.post_set.get(pk=post_pk)

            post.delete()
            return Response(f"Post-{post.id} deleted successfully")
        except Author.DoesNotExist:
            return Response(f"Author of id-{author_pk} doesn't exist", status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            return Response(f"Author of id-{author_pk} doesn't have this post", status=status.HTTP_404_NOT_FOUND)


@ api_view(['GET', 'POST'])
@ parser_classes([MultiPartParser, FormParser])
# Return a list of Post or to create a post with incremental ID
def posts(request, author_pk):
    if request.method == 'GET':
        try:
            author = Author.objects.get(pk=author_pk)
            posts = author.post_set.all()

            page_number = request.GET.get('page')
            size = request.GET.get('size')

            if page_number and size:
                paginator = Paginator(posts, size)
                posts = paginator.get_page(page_number).object_list
            postsData = PostSerializer(posts, many=True).data

            return Response(postsData)
        except Author.DoesNotExist:
            return Response('Author doesn\'t exist', status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        try:
            author = Author.objects.get(pk=author_pk)
        except Author.DoesNotExist:
            return Response("Author doesn't exist", status=status.HTTP_404_NOT_FOUND)

        # You can only make a post if the logged in user is the author
        if not request.user.is_authenticated or request.user.id != author.user_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                return create_post(request, author)
            except Author.DoesNotExist:
                return Response('Author doesn\'t exist', status=status.HTTP_404_NOT_FOUND)


# Helper method to create a post
def create_post(request, author, id=None):
    try:
        # Do something with the image file here to create an image post
        if request.data.get('imageFile'):
            imageFile = request.data.get('imageFile').file

        # Grab category data
        category_list = []
        for category in request.data.getlist('categories'):
            category_obj, created = Category.objects.get_or_create(
                name=category)
            category_list.append(category_obj)

        cpy = request.data.copy()
        author_serializer = AuthorSerializer(author)
        category_serializer = CategorySerializer(category_list, many=True)

        # TODO: Use proper values later when implementing post sharing
        cpy['source'] = "https://temp.com"
        cpy['origin'] = "https://temp.com"

        if id:
            cpy['id'] = id

        post_serializer = PostSerializer(data=cpy)
        if post_serializer.is_valid():
            post_serializer.save(author=author_serializer.data,
                                 categories=category_serializer.data)
            return Response(post_serializer.data)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
