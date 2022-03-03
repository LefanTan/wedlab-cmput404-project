import uuid
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from service.serializers import AuthorSerializer, PostSerializer, FollowRequestSerializer
from .models import Author, InboxObject, Post, FollowRequest


def serialize_inbox_item(item):
    model = item.content_type.model_class()
    if model is Post:
        serializer = PostSerializer
    elif model is FollowRequest:
       serializer = FollowRequestSerializer
    # elif model is Like:
    #    serializer = LikeSerializer
    return serializer(item.content_object).data


def get_inbox_object(data):
    type = data['type']
    if type == 'post':
        object = Post.objects.get(pk=data['id'])
    elif type == 'Follow':
       object = FollowRequest.objects.get(pk=data['id'])
    # elif type == 'Like':
    #    object = Like.objects.get(pk=data['id'])
    return object


@api_view(['GET', 'POST'])
# Return a list of posts in inbox
def inbox_list(request, pk):
    if request.method == 'GET':
        try:
            author = Author.objects.get(pk=pk)
        except:
            return Response("Author doesn't exist", status=status.HTTP_404_NOT_FOUND)
        author_url = AuthorSerializer(author).data['id']

        # Authors can only view their own inbox
        if not request.user.is_authenticated or request.user.id != author.user_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        inbox_list = InboxObject.objects.filter(author=author)
        data = [serialize_inbox_item(obj) for obj in inbox_list]
        return Response({"type": "inbox", "author": author_url, "items": data})

    if request.method == 'POST':
        try:
            author = Author.objects.get(pk=pk)
        except:
            return Response("Author doesn't exist", status=status.HTTP_404_NOT_FOUND)

        item = get_inbox_object(request.data)
        if item:
            # create an InboxObject which links to target author
            inbox_item = InboxObject(content_object=item, author=author)
            inbox_item.save()
            return Response({'request': request.data, 'saved': model_to_dict(inbox_item)})
        return Response(status=status.HTTP_400_BAD_REQUEST)
