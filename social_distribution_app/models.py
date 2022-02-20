from django.db import models


# Reference: https://stackoverflow.com/questions/45710889/list-field-in-model-django
class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
       return self.category


class Author(models.Model):
    id = models.CharField(max_length=1000, primary_key=True)
    type = models.CharField(max_length=1000)
    displayName = models.CharField(max_length=1000)
    url = models.URLField(max_length=1000)
    host = models.CharField(max_length=1000)
    github = models.URLField(max_length=1000)
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


    title = models.CharField(max_length=1000)
    id = models.URLField(max_length=1000, primary_key=True)
    source = models.URLField(max_length=1000)
    origin = models.URLField(max_length=1000)
    description = models.CharField(max_length=1000)
    contentType = models.CharField(max_length=1000)
    imageSource = models.URLField(max_length=1000)
    authorId = models.CharField(max_length=1000)
    category = models.ManyToManyField(Category)
    count = models.IntegerField(max_length=1000)
    comments = models.URLField(max_length=1000)
    publishedDate = models.DateTimeField(max_length=1000, auto_now=True)
    visibility = models.CharField(max_length=2, choices=VISIBILITY_CHOICES, default=PUBLIC)
    unlisted = models.BooleanField(max_length=1000)
