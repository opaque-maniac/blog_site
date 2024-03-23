from django.urls import path

from .views import CreateComplaintView

app_name = 'core'

# URLs for the core application
urlpatterns = [
    path('complaints/', CreateComplaintView.as_view(), name='create-complaint'),
]
