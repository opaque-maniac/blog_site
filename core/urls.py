from django.urls import path

from .views import (
    home,
    about,
    contact,
    terms
)

app_name = 'core'

# URLs for the core app
urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('terms/', terms, name='terms'),
]
