from django.urls import path, include
from service import author_views, post_views

urlpatterns = [
    path('auth/signup/', author_views.signup, name='signup'),
    path('service/', include([
        # Author Endpoints
        path('authors/', author_views.author_list, name='author_list'),
        path('authors/<str:pk>', author_views.author_detail, name='author_detail'),

        # Post Endpoints
        path('authors/<str:author_pk>/posts/<str:post_pk>',
             post_views.post_detail, name='post_detail'),
        path('authors/<str:author_pk>/posts',
             post_views.posts, name='post_list')
    ]))
]
