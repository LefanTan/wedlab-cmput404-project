from unicodedata import category
from datetime import date, datetime
import markdown
from rest_framework import serializers
from .models import Author, Category, InboxObject, Post, FollowRequest
from django.contrib.auth.models import User


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

        # TODO: Temporary comment data!
        # ret['commentsSrc'] = {
        #     "comments": [
        #         {
        #             "type": "comment",
        #             "author": {
        #                 "type": "author",
        #                 # ID of the Author (UUID)
        #                 "id": "http://127.0.0.1:8000/authors/1d698d25ff008f7538453c120f581471",
        #                 # url to the authors information
        #                 "url": "http://127.0.0.1:8000/authors/1d698d25ff008f7538453c120f581471",
        #                 "host": "http://127.0.0.1:8000/",
        #                 "displayName": "Greg Johnson",
        #                 # HATEOS url for Github API
        #                 "github": "http://github.com/gjohnson",
        #                 # Image from a public domain
        #                 "profileImage": "https://i.imgur.com/k7XVwpB.jpeg"
        #             },
        #             "comment": "**Comment** with markdown!",
        #             "contentType": "text/markdown",
        #             # ISO 8601 TIMESTAMP
        #             "published": "2015-03-09T13:07:04+00:00",
        #             # ID of the Comment (UUID)
        #             "id": "http://127.0.0.1:8000/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
        #         },
        #         {
        #             "type": "comment",
        #             "author": {
        #                 "type": "author",
        #                 # ID of the Author (UUID)
        #                 "id": "http://127.0.0.1:8000/authors/4cee67d276f048559e27c7e800e388c3",
        #                 # url to the authors information
        #                 "url": "http://127.0.0.1:8000/authors/4cee67d276f048559e27c7e800e388c3",
        #                 "host": "http://127.0.0.1:8000/",
        #                 "displayName": "lefan2",
        #                 # HATEOS url for Github API
        #                 "github": "http://github.com/gjohnson",
        #                 # Image from a public domain
        #                 "profileImage": ""
        #             },
        #             "comment": "Sick Olde English",
        #             "contentType": "text/plain",
        #             # ISO 8601 TIMESTAMP
        #             "published": "2015-03-09T13:07:04+00:00",
        #             # ID of the Comment (UUID)
        #             "id": "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
        #         }
        #     ]
        # }
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
