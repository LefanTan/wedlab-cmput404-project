from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    displayName = models.CharField(max_length=255)
    url = models.URLField(max_length=500)
    host = models.URLField(max_length=500)
    github = models.URLField(max_length=500)
    profileImage = models.URLField(max_length=500)


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

    # Choices for categories
    # CATEGORY_CHOICES = []

    title = models.CharField(max_length=1000)
    id = models.AutoField(primary_key=True)
    source = models.URLField(max_length=1000)
    origin = models.CharField(max_length=1000)
    contentType = models.CharField(max_length=1000)
    imageSource = models.URLField(max_length=1000)
    authorId = models.ForeignKey(
        Author, on_delete=models.CASCADE)
    # category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=)
    count = models.IntegerField()
    comments = models.CharField(max_length=1000)
    publishedDate = models.DateTimeField(max_length=1000, auto_now=True)
    visibility = models.CharField(
        max_length=2, choices=VISIBILITY_CHOICES, default=PUBLIC)
    unlisted = models.BooleanField(max_length=1000)
