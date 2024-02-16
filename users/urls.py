from django.urls import path

from .views import (
    register_view,
    login_view,
    logout_view,
    profile,
    update_profile,
)

app_name = 'users'

# URLs for the users app
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
]
