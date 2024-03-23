from django.urls import path

from .views import CreateComplaintView, ExploreView

app_name = 'core'

# URLs for the core application
urlpatterns = [
    path('complaints/', CreateComplaintView.as_view(), name='create-complaint'),
    path('explore/', ExploreView.as_view(), name='explore'),
]
