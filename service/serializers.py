from rest_framework import serializers
from .models import Author


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'type', 'displayName',
                  'url', 'host', 'github', 'profileImage']
