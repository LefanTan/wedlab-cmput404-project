from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from service.serializers import PostSerializer, ImagePostSerializer
from .models import Author, Post

@swagger_auto_schema(method='get', operation_description="Return image from a post if exists")
@ api_view(['GET'])
# Return image from a post if exists
def imagepost(request, author_pk, post_pk):

    if request.method == 'GET':
        try:
            author = Author.objects.get(pk=author_pk)
            post = author.post_set.get(pk=post_pk)
            imageURL= PostSerializer(post, many=False).data["imageSource"]

            if imageURL is not None:
                imageData = ImagePostSerializer(imageURL).data
                return Response(imageData)
            else:
                return Response('Image doesn\'t exist', status=status.HTTP_404_NOT_FOUND)
                
        except Author.DoesNotExist:
            return Response('Author doesn\'t exist', status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            return Response('Post doesn\'t exist', status=status.HTTP_404_NOT_FOUND)