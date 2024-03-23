from django.urls import path

from .views import (
    Registerview,
    LoginView,
    UserProfileView,
    UserPostsView,
)

app_name = 'users'

# URLs for the users application
urlpatterns = [
    path('register/', Registerview.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/posts/', UserPostsView.as_view(), name='profile-posts'),
]
