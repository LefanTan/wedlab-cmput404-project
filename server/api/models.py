from django.db import models

# Create your models here.


class Author(models.Model):
    displayName = models.CharField(max_length=100)
    admin = models.BooleanField(default=False)
