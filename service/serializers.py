from rest_framework import serializers
from .models import Author, Category, Post


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['type', 'id', 'displayName',
                  'url', 'host', 'github', 'profileImage']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['id'] = ret['url']
        return ret


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ['categories', 'uuid']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']
