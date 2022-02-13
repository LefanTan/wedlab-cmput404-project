from django.db import models


class Author(models.Model):
    id = models.CharField(primary_key=True)
    type = models.CharField()
    displayName = models.CharField()
    url = models.URLField()
    host = models.CharField()
    github = models.URLField()
    profileImage = models.ImageField()


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

    title = models.CharField()
    id = models.CharField(primary_key=True)
    source = models.URLField()
    origin = models.CharField()
    contentType = models.CharField()
    imageSource = models.URLField()
    authorId = models.CharField()
    # category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=)
    count = models.IntegerField()
    comments = models.CharField()
    publishedDate = models.DateTimeField(auto_now=True)
    visibility = models.CharField(max_length=2, choices=VISIBILITY_CHOICES, default=PUBLIC)
    unlisted = models.BooleanField()
