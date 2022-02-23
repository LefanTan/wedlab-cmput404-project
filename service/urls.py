from django.urls import path, include
from service import views

urlpatterns = [
    path('auth/signup/', views.signup, name='signup'),
    path('service/', include([
        # Author Endpoints
        path('authors/', views.author_list),
        path('authors/<str:pk>', views.author_detail),

        # Post Endpoints
        path('authors/<str:author_pk>/posts/<str:post_pk>', views.post_detail),
        path('authors/<str:author_pk>/posts', views.posts)
    ]))
]
