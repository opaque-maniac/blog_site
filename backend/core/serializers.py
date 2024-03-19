from rest_framework import serializers
from .models import Complaint

# Complaint serializer for complaints
class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['email', 'name', 'message']
