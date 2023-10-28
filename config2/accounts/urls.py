from django.urls import path

from .views import register
from .views import login
from .views import logout

app_name = 'accounts'

#urls for this app
urlpatterns = [
    path('signup/', register, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]