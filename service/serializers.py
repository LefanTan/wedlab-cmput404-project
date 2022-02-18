from rest_framework import serializers
from .models import Author, Post


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'type', 'displayName',
                  'url', 'host', 'github', 'profileImage']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'source',
                  'origin', 'contentType', 'imageSource', 'authorId',
                  'count', 'comments', 'publishedDate', 'visibility', 'unlisted']
