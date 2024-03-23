from rest_framework import permissions, generics

from .serializer import ComplaintCreateSerialzier

# View for creating a complaint
class CreateComplaintView(generics.CreateAPIView):
    serializer_class = ComplaintCreateSerialzier
    permission_classes = [permissions.AllowAny]