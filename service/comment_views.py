from uuid import uuid4
import uuid
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_yasg.utils import swagger_auto_schema

from service.serializers import AuthorSerializer, PostSerializer, CommentSerializer
from .models import Author, Post, Comment


@ api_view(['GET', 'POST'])
@ parser_classes([MultiPartParser, FormParser])
def comments(request, author_pk, post_pk):

    if request.method == 'GET':
        try:
            page_number = request.GET.get('page')
            size = request.GET.get('size')

            author = Author.objects.get(pk=author_pk)
            post = author.post_set.get(pk=post_pk)
            comments = post.comment_set.all().order_by('-publishedDate')

            if page_number and size:
                paginator = Paginator(comments, size)
                comments = paginator.get_page(page_number).object_list
            commentsData = CommentSerializer(comments, many=True).data

            return Response(commentsData)
        except Author.DoesNotExist:
            return Response('Author doesn\'t exist', status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            return Response('Post doesn\'t exist', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        try:
            cp = request.data.copy()
            cp['id'] = uuid4().hex
            cp['url'] = f"{request.build_absolute_uri('/')}authors/{author_pk}/posts/{post_pk}/comments/{cp.get('id')}"
            cp['content'] = cp.get('comment')

            comment_serializer = CommentSerializer(data=cp)
            if comment_serializer.is_valid():
                comment_serializer.save(
                    author=Author.objects.get(pk=author_pk),
                    post=Post.objects.get(pk=post_pk)
                )

                return Response(comment_serializer.data)
            else:
                return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Author.DoesNotExist:
            return Response('Author doesn\'t exist', status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            return Response('Post doesn\'t exist', status=status.HTTP_404_NOT_FOUND)