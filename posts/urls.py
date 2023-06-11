from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('detail/<slug:post_slug>/', views.PostDetailView.as_view(), name='detail'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='profile'),
    path('like/post/<int:post_id>/', views.VoteView.as_view(), name='post_like'),
    path('comment/like/<int:comment_id>/',
         views.VoteView.as_view(), name='comment_like'),
    path('post/delete/<int:post_id>/',
         views.PostDeleteView.as_view(), name='post_delete'),
    path('post/update/<int:post_id>/',
         views.PostUpdateView.as_view(), name='post_update'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
]
