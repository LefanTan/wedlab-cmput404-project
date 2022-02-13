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


