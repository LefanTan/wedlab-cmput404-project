from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('post/create', post_form, name='post_create'),
    path('post/edit', post_form, name='post_edit')
]
