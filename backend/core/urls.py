from django.urls import path
from .views import ComplaintView, CSRFView

urlpatterns = [
    path('complaint/', ComplaintView.as_view(), name='complaint'),
    path('csrf/', CSRFView.as_view(), name='csrf'),
]
