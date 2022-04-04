from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


def generate_uuid_hex():
    return uuid.uuid4().hex


class Author(models.Model):
    id = models.CharField(
        primary_key=True, default=generate_uuid_hex, max_length=250)
    type = models.CharField(default="author", max_length=125)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayName = models.CharField(max_length=255, unique=True)
    url = models.URLField(max_length=250)
    host = models.URLField(max_length=250)
    github = models.URLField(max_length=250)
    profileImage = models.URLField(max_length=250, null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class InboxObject(models.Model):
    id = models.CharField(primary_key=True, editable=False,
                          default=generate_uuid_hex, max_length=250)
    # the author that the object (follow, like, post) is sent to
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.CharField(max_length=250, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')


class Post(models.Model):
    # Choices for visibilities
    PUBLIC = 'PUBLIC'
    FRIENDS = 'FRIENDS'
    PRIVATE = 'PRIVATE'
    AUTHORIZED_USER = 'AUTHORIZED'
    VISIBILITY_CHOICES = [
        (PUBLIC, 'Public'),
        (FRIENDS, 'Friends-Only'),
        (PRIVATE, 'Private'),
        (AUTHORIZED_USER, 'Authorized users')
    ]

    # Choices for content-type
    MARKDOWN = 'text/markdown'
    PLAIN = 'text/plain'
    BASE64 = 'application/base64'
    PNG = 'image/png;base64'
    JPEG = 'image/jpeg;base64'
    CONTENT_TYPES = [
        (MARKDOWN, 'text/markdown'),
        (PLAIN, 'text/plain'),
        (BASE64, 'application/base64'),
        (PNG, 'image/png;base64'),
        (JPEG, 'image/jpeg;base64'),
    ]

    id = models.CharField(
        primary_key=True, default=generate_uuid_hex, max_length=250)
    title = models.CharField(max_length=250)
    type = models.CharField(default="post", max_length=125)
    description = models.CharField(max_length=500)
    source = models.URLField(max_length=250)
    origin = models.CharField(max_length=250)
    contentType = models.CharField(
        max_length=50, choices=CONTENT_TYPES, default=PLAIN)
    imageSource = models.URLField(max_length=500, null=True, blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    publishedDate = models.DateTimeField(max_length=250, auto_now=True)
    visibility = models.CharField(
        max_length=25, choices=VISIBILITY_CHOICES, default=PUBLIC)
    unlisted = models.BooleanField(default=False)
    inbox_object = GenericRelation(InboxObject, on_delete=models.CASCADE)


class FollowRequest(models.Model):
    id = models.CharField(
        primary_key=True, default=generate_uuid_hex, max_length=250)
    summary = models.CharField(max_length=500)
    type = models.CharField(default="Follow", max_length=125)
    actor = models.ForeignKey(
        Author, on_delete=models.CASCADE, unique=False)
    object = models.CharField(max_length=250, null=True)
    inbox_object = GenericRelation(InboxObject, on_delete=models.CASCADE)


class Comment(models.Model):
    type = models.CharField(default="comment", max_length=100)
    id = models.CharField(
        primary_key=True, default=generate_uuid_hex, max_length=250)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, null=True)
    contentType = models.CharField(max_length=50, default='text/plain')
    publishedDate = models.DateTimeField(max_length=250, auto_now=True)
    url = models.URLField(max_length=250)


class Upload(models.Model):
    uploadedDate = models.DateTimeField(auto_now_add=True)
    file = models.FileField(max_length=500)


class Host(models.Model):
    allowed = models.BooleanField(default=True)
    url = models.URLField(max_length=250)
    name = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
