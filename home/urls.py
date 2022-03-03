from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('authors/<str:author_pk>', profile, name='profile'),
    path('authors/<str:author_pk>/posts', post_list, name='home_post_list'),
    path('sendfollowrequest', follow_request, name='follow_request'),
    path('post/create', post_create, name='home_post_create'),

    path('post/<str:post_pk>/edit', post_edit, name='home_post_edit'),
    path('post/<str:post_pk>/share', share_post, name='share_post'),
    path('inbox/messages', messages, name='messages'),
    path('inbox/requests', requests, name='requests')
]
