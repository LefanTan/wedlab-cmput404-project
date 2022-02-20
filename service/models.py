from django.db import models
from django.contrib.auth.models import User
import uuid


def generate_uuid_hex():
    return uuid.uuid4().hex


class Author(models.Model):
    uuid = models.CharField(default=generate_uuid_hex, max_length=250)
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayName = models.CharField(max_length=255)
    url = models.URLField(max_length=250)
    host = models.URLField(max_length=250)
    github = models.URLField(max_length=250)
    profileImage = models.URLField(max_length=250)


class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Post(models.Model):
    # Choices for visibilities
    PUBLIC = 'PU'
    FRIENDS = 'FO'
    PRIVATE = 'PR'
    AUTHORIZED_USER = 'AU'
    VISIBILITY_CHOICES = [
        (PUBLIC, 'Public'),
        (FRIENDS, 'Friends-Only'),
        (PRIVATE, 'Private'),
        (AUTHORIZED_USER, 'Authorized users')
    ]

    title = models.CharField(max_length=250)
    uuid = models.CharField(default=generate_uuid_hex, max_length=250)
    id = models.AutoField(primary_key=True)
    source = models.URLField(max_length=250)
    origin = models.CharField(max_length=250)
    contentType = models.CharField(max_length=125)
    imageSource = models.URLField(max_length=250)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    publishedDate = models.DateTimeField(max_length=250, auto_now=True)
    visibility = models.CharField(
        max_length=2, choices=VISIBILITY_CHOICES, default=PUBLIC)
    unlisted = models.BooleanField(default=False)
