from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('post/create', post_create, name='post_create'),
    path('post/<str:post_pk>/edit', post_edit, name='post_edit')
]
