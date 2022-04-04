from uuid import uuid4
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from drf_yasg.utils import swagger_auto_schema
from service.serializers import AuthorSerializer, PostSerializer, CommentSerializer, LikePostSerializer, LikeCommentSerializer
from .models import Author, Post, Comment, LikePost, LikeComment

@swagger_auto_schema(method='get', operation_description="Retrieve existing likes of a post")
@swagger_auto_schema(method='post', operation_description="Add like to a post")
@ api_view(['GET', 'POST'])
@ parser_classes([MultiPartParser, FormParser])
def like_post(request, author_pk, post_pk):

    if request.method == 'GET':
        try:
            page_number = request.GET.get('page')
            size = request.GET.get('size')

            author = Author.objects.get(pk=author_pk)
            post = author.post_set.get(pk=post_pk)
            post_id = PostSerializer(post).data["id"]
            likes = LikePost.objects.all().filter(post_id=post_id)

            if page_number and size:
                paginator = Paginator(likes, size)
                likes = paginator.get_page(page_number).object_list
            likesData = LikePostSerializer(likes, many=True).data

            return Response(likesData)
        except Author.DoesNotExist:
            return Response('Author doesn\'t exist', status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            return Response('Post doesn\'t exist', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        try:
            author = Author.objects.get(pk=author_pk)
            author_name_who_liked = AuthorSerializer(author, many=False).data["displayName"]

            cpy = request.data.copy()
            cpy['url'] = f"{request.build_absolute_uri('/')}authors/{author_pk}/posts/{post_pk}"
            cpy['summary'] = f"{author_name_who_liked} likes your post"
            cpy['post_id'] = f"{post_pk}"

            LikePost_serializer = LikePostSerializer(data=cpy)
            if LikePost_serializer.is_valid():
                LikePost_serializer.save(
                    author=Author.objects.get(pk=author_pk)
                )

                return Response(LikePost_serializer.data)
            else:
                return Response(LikePost_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Author.DoesNotExist:
            return Response('Author doesn\'t exist', status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            return Response('Post doesn\'t exist', status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(method='get', operation_description="Retrieve existing likes of a comment")
@swagger_auto_schema(method='post', operation_description="Add like to a comment")
@ api_view(['GET', 'POST'])
@ parser_classes([MultiPartParser, FormParser])
def like_comment(request, author_pk, post_pk, comment_pk):

    if request.method == 'GET':
        try:
            page_number = request.GET.get('page')
            size = request.GET.get('size')

            author = Author.objects.get(pk=author_pk)
            post = author.post_set.get(pk=post_pk)
            comment = post.comment_set.get(pk=comment_pk)
            comment_id = CommentSerializer(comment).data["id"]
            likes = LikeComment.objects.all().filter(comment_id=comment_id)

            if page_number and size:
                paginator = Paginator(likes, size)
                likes = paginator.get_page(page_number).object_list
            likesData = LikeCommentSerializer(likes, many=True).data

            return Response(likesData)
        except Author.DoesNotExist:
            return Response('Author doesn\'t exist', status=status.HTTP_404_NOT_FOUND)
        except Comment.DoesNotExist:
            return Response('Comment doesn\'t exist', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        try:
            author = Author.objects.get(pk=author_pk)
            author_name_who_liked = AuthorSerializer(author, many=False).data["displayName"]

            cpy = request.data.copy()
            cpy['url'] = f"{request.build_absolute_uri('/')}authors/{author_pk}/posts/{post_pk}/comments/{comment_pk}"
            cpy['summary'] = f"{author_name_who_liked} likes your comment"
            cpy['comment_id'] = f"{comment_pk}"

            LikeComment_serializer = LikeCommentSerializer(data=cpy)
            if LikeComment_serializer.is_valid():
                LikeComment_serializer.save(
                    author=Author.objects.get(pk=author_pk)
                )

                return Response(LikeComment_serializer.data)
            else:
                return Response(LikeComment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Author.DoesNotExist:
            return Response('Author doesn\'t exist', status=status.HTTP_404_NOT_FOUND)
        except Comment.DoesNotExist:
            return Response('Comment doesn\'t exist', status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(method='get', operation_description="Retrieve existing likes of an author")
@ api_view(['GET'])
@ parser_classes([MultiPartParser, FormParser])
def author_liked(request, author_pk):
    if request.method == 'GET':
        try:
            author = Author.objects.get(pk=author_pk)

            post_likes = LikePost.objects.all().filter(author=author)
            post_likesData = LikePostSerializer(post_likes, many=True).data
            comment_likes = LikeComment.objects.all().filter(author=author)
            comment_likesData = LikeCommentSerializer(comment_likes, many=True).data

            finalData = {"type": "liked", "items": post_likesData + comment_likesData}

            return Response(finalData)
        except Author.DoesNotExist:
            return Response('Author doesn\'t exist', status=status.HTTP_404_NOT_FOUND)