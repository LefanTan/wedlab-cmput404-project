import uuid
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema

from service.serializers import AuthorSerializer, FollowRequestSerializer
from .models import Author, FollowRequest, InboxObject


@swagger_auto_schema(method='get', operation_description="Get a list of followers")
@api_view(['GET'])
def follower_list(request, author_pk):
    try:
        author = Author.objects.get(pk=author_pk)
    except Author.DoesNotExist:
        return Response("Author doens't exist", status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        detail = FollowRequest.objects.all().filter(object=author.id, summary="accepted").values_list('actor_id')
        follow_list = Author.objects.all().filter(pk__in=detail)

        page_number = request.GET.get('page')
        size = request.GET.get('size')

        if page_number and size:
            paginator = Paginator(follow_list, size)
            follow_list = paginator.get_page(page_number).object_list
        data = AuthorSerializer(follow_list, many=True).data

        return Response({"type": "followers", "items": data})


@swagger_auto_schema(method='get', operation_description="Get the detail of the current follower")
@swagger_auto_schema(method='put', operation_description="Add the current author as the follower")
@swagger_auto_schema(method='delete', operation_description="Remove the current follower")
@api_view(['GET', 'PUT', 'DELETE'])
def follower_detail(request, author_pk, foreign_author_pk):
    try:
        current = Author.objects.get(pk=author_pk)
        foreign = Author.objects.get(pk=foreign_author_pk)
    except Author.DoesNotExist:
        return Response("Author doens't exist", status=status.HTTP_404_NOT_FOUND)

    # Get the current follower detail
    if request.method == 'GET':
        serializer = AuthorSerializer(foreign)
        return Response(serializer.data)

    # Unfollow the current follower
    if request.method == 'DELETE':
        try:
            follower = FollowRequest.objects.get(actor=foreign_author_pk)
            name = Author.objects.get(pk=foreign_author_pk).displayName

            follower.delete()
            return Response(f"Unfollow {name} successfully")
        except Author.DoesNotExist:
            return Response(f"Author of id-{author_pk} doesn't exist", status=status.HTTP_404_NOT_FOUND)

    # Follow the current author
    if request.method == 'PUT':
        try:
            followSet = FollowRequest.objects.all().filter(object=current.id, summary="accepted")
            ready = Author.objects.get(pk=foreign_author_pk)
            newName = ready.displayName

            if ready not in followSet:
                return sendRequest(author_pk, foreign_author_pk)
            elif ready in followSet:
                if followSet.filter(actor=author_pk, object=foreign_author_pk):
                    return Response(f"You've sent follow request to {newName}")
                elif followSet.filter(actor=author_pk, object=foreign_author_pk, summary='accepted'):
                    return Response(f"{newName} is your follower")

        except Author.DoesNotExist:
            return Response(f"Author of id-{author_pk} doesn't exist", status=status.HTTP_404_NOT_FOUND)


def sendRequest(author_pk, foreign_pk):
    try:
        sender = Author.objects.get(pk=foreign_pk)  # Sender
        receiver = Author.objects.get(pk=author_pk)  # Receiver
        allRequests = FollowRequest.objects.all().filter(actor_id=foreign_pk).values_list('actor')

        if sender.id not in allRequests:
            data = {
                'id': uuid.uuid4().hex,
                'summary': f"{receiver.displayName} wants to invite you as a follower",
                'type': 'Follow',
                'actor': sender.id,
                'object': receiver.id
            }

            follow_serializer = FollowRequestSerializer(data=data)

            if follow_serializer.is_valid():
                follow_serializer.save()

                # Send the request data to the receiver's inbox
                object = FollowRequest.objects.get(pk=data['id'])
                inbox_item = InboxObject(content_object=object, author=sender)
                inbox_item.save()
                # , model_to_dict(inbox_item)
                return Response(follow_serializer.data)
            return Response("Data not valid", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You've sent request to this author!", status=status.HTTP_400_BAD_REQUEST)

    except Author.DoesNotExist:
        return Response("Username does not exist!", status=status.HTTP_400_BAD_REQUEST)