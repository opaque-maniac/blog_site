from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('profile/', views.ProfileAPIView.as_view(), name='profile'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),
]
