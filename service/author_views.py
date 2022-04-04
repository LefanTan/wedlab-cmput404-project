import uuid
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

from service.serializers import AuthorSerializer
from .models import Author


@swagger_auto_schema(method='get', auto_schema=None)
@swagger_auto_schema(method='post', operation_description="Signs an author up. A new author and user object will be created.")
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

            # Create Author object
            cp = body.copy()
            cp['id'] = uuid.uuid4().hex
            cp['host'] = request.build_absolute_uri('/')
            cp['url'] = f"{cp.get('host')}authors/{cp.get('id')}"
            cp['displayName'] = cp.get('username')

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


def author_login(request):
    if request.method == 'POST':
        try:
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password'])
            if user is not None:
                author = Author.objects.get(user_id=user.id)
                if user.is_active and author.approved:
                    login(request, user)
                    return redirect('home')
                else:
                    return redirect('login')
            else:
                return redirect('login')
        except Exception as e:
            print(e)
            return redirect('login')
    if request.method == 'GET':
        return render(request, 'registration/login.html')


@swagger_auto_schema(method='get', operation_description="Get a list of author")
@api_view(['GET'])
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


@swagger_auto_schema(method='get', operation_description="Get a specific author")
@swagger_auto_schema(method='post', operation_description="Update a specific of author")
@api_view(['GET', 'POST'])
@parser_classes([FormParser, MultiPartParser])
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
            displayName = request.data.get('displayName')

            if password:
                request.user.set_password(password)

            if displayName:
                request.user.username = displayName
                request.user.save()

            serializer = AuthorSerializer(
                author, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
