from unicodedata import category
from wsgiref import validate
from rest_framework import serializers
from .models import Author, Category, Post
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False, many=False)

    class Meta:
        model = Author
        fields = ['type', 'id', 'displayName', 'user', 'uuid',
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
        ret.pop('uuid')
        return ret


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, required=False)
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
