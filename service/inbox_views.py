import uuid
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from service.serializers import AuthorSerializer, InboxObjectSerializer, PostSerializer
from .models import Author, InboxObject, Post


def serialize_inbox_item(item, context={}):
        model = item.content_type.model_class()
        if model is Post:
            serializer = PostSerializer   
        #elif model is FollowRequest:
        #    serializer = FollowRequestSerializer
        #elif model is Like:
        #    serializer = LikeSerializer
        return serializer(item.content_object, context=context).data

@ api_view(['GET'])
# Return a list of posts in inbox
def inbox_list(request, pk):
    if request.method == 'GET':
        try:
            author = Author.objects.get(pk=pk)
        except:
            return Response("Author doesn't exist", status=status.HTTP_404_NOT_FOUND)
        inbox_list = InboxObject.objects.filter(author=author)
        data = [serialize_inbox_item(obj) for obj in inbox_list]
        return Response({"type": "inbox", "author": pk, "items": data})

