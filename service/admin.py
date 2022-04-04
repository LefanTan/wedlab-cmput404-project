from django.contrib import admin
from .models import Host, Author,FollowRequest

admin.site.register(Host)
admin.site.register(Author)
admin.site.register(FollowRequest)
