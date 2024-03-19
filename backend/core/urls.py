from django.urls import path
from .views import ComplaintView

urlpatterns = [
    path('complaint/', ComplaintView.as_view(), name='complaint'),
]
