from django.urls import path
from service import views

urlpatterns = [
    # Author Endpoints
    path('authors/', views.author_list),
    path('authors/<int:pk>', views.author_detail),

    # Post Endpoints
    path('authors/<int:author_pk>/posts/<int:post_pk>', views.posts)
]
