from django.contrib import admin
from .models import Host, FollowRequest, Author

admin.site.register(Host)
admin.site.register(FollowRequest)
admin.site.register(Author)
