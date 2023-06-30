from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from . import views


app_name = 'api'
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/', views.UserRegisterView.as_view()),
    path('user/update/<int:pk>/', views.UserUpdateView.as_view()),
    path('user/delete/<int:pk>/', views.UserDeleteView.as_view()),
    path('user/', views.UserView.as_view()),
    path('post/detail/<int:pk>/', views.PostDetailView.as_view()),
    path('post/create/', views.PostCreateView.as_view()),
    path('post/update/<int:pk>/', views.PostUpdateView.as_view()),
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view()),
    path('vote/<int:pk>/', views.VoteView.as_view()),
]
