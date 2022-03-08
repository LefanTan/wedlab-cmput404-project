from unicodedata import category
from datetime import date, datetime
import markdown
from rest_framework import serializers
from .models import Author, Category, InboxObject, Post, FollowRequest, Comment
from django.contrib.auth.models import User
from django_base64field.fields import Base64Field
import base64
import requests


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False, many=False)

    class Meta:
        model = Author
        fields = ['type', 'id', 'displayName', 'user',
                  'url', 'host', 'github', 'profileImage']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_obj = User.objects.create_user(**user_data)

        author = Author.objects.create(
            **validated_data, user=user_obj)
        return author

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['id'] = ret['url']
        ret.pop('user')
        return ret


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, required=False, read_only=True)
    categories = serializers.SlugRelatedField(
        slug_field='name', read_only=True, many=True)

    class Meta:
        model = Post
        fields = '__all__'
        depth = 2

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        categories_data = validated_data.pop('categories')

        author_obj = Author.objects.get(url=author_data.get('url'))
        category_obj_list = []
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(**category_data)
            category_obj_list.append(category)

        post = Post.objects.create(
            **validated_data, author=author_obj)
        post.categories.set(category_obj_list)
        post.save()
        return post

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        comments = Comment.objects.filter(post=instance)
        ret["comments"] = CommentSerializer(comments, many=True).data
        return ret


class InboxObjectSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, required=True)
    object = serializers.JSONField()

    class Meta:
        model = InboxObject
        fields = ['author', 'object']

    def create(self, validated_data):
        return InboxObject.objects.create(**validated_data)

    def to_representation(self, instance):
        # the representation is the json object
        return super().to_representation(instance)


class FollowRequestSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, required=False)

    class Meta:
        model = FollowRequest
        fields = '__all__'

    def create(self, validated_data):
        followId = validated_data.pop('id')
        follow = FollowRequest.objects.create(**validated_data, id=followId)
        follow.save()
        return follow

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(required=False)

    class Meta:
        model = Comment
        exclude = ['post']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['id'] = ret['url']
        ret.pop('url')
        return ret

class ImagePostSerializer(serializers.Serializer):
    image_base64 = Base64Field(blank=True, null=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["image_base64"] = base64.b64encode(requests.get(instance).content)
        return ret
