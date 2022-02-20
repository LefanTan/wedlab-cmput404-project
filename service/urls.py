from django.urls import path, include
from service import views

urlpatterns = [
    path('auth/signup/', views.signup, name='signup'),
    path('service/', include([
        # Author Endpoints
        path('authors/', views.author_list),
        path('authors/<int:pk>', views.author_detail),

        # Post Endpoints
        path('authors/<int:author_pk>/posts/<int:post_pk>', views.posts)
    ]))
]
