from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    ProfileView,
)

app_name = 'users'

# URLs for the users application
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
]
