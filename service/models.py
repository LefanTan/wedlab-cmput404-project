from django.db import models
from django.contrib.auth.models import User
import uuid


def generate_uuid_hex():
    return uuid.uuid4().hex


class Author(models.Model):
    id = models.CharField(
        primary_key=True, default=generate_uuid_hex, max_length=250)
    type = models.CharField(default="author", max_length=125)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayName = models.CharField(max_length=255)
    url = models.URLField(max_length=250)
    host = models.URLField(max_length=250)
    github = models.URLField(max_length=250)
    profileImage = models.URLField(max_length=250, null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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
    imageSource = models.URLField(max_length=250, null=True, blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    publishedDate = models.DateTimeField(max_length=250, auto_now=True)
    visibility = models.CharField(
        max_length=25, choices=VISIBILITY_CHOICES, default=PUBLIC)
    unlisted = models.BooleanField(default=False)
