from rest_framework import serializers
from .models import Author, Post


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'displayName',
                  'url', 'host', 'github', 'profileImage']

    # def create(self, validated_data):
    #     validated_data.id = validated_data.url
    #     return Author.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     """
    #     Update and return an existing `Snippet` instance, given the validated data.
    #     """
    #     instance.id = validated_data.get('url', instance.url)
    #     instance.save()
    #     return instance


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'source',
                  'origin', 'contentType', 'imageSource', 'author', 'publishedDate', 'visibility', 'unlisted']
