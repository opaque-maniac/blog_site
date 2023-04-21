from django.urls import path
from .views import SignUpView

#urls for this app
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]