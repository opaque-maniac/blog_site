from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.middleware.csrf import get_token

from .models import Complaint
from .serializers import ComplaintSerializer

# View for sending complaints
class ComplaintView(generics.CreateAPIView):
    serializer_class = ComplaintSerializer
    queryset = Complaint.objects.all()
    permission_classes = [permissions.AllowAny]

# View for getting a csrf token
class CSRFView(APIView):
    def get(self, request):
        return Response({'csrfToken': get_token(request)})