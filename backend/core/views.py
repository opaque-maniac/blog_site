from rest_framework import generics, permissions

from .models import Complaint
from .serializers import ComplaintSerializer

# View for sending complaints
class ComplaintView(generics.CreateAPIView):
    serializer_class = ComplaintSerializer
    queryset = Complaint.objects.all()
    permission_classes = [permissions.AllowAny]