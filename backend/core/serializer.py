from rest_framework import serializers
from validate_email import validate_email
import re

from .models import Complaints

# Seraializer for submitting a complaint
class ComplaintCreateSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Complaints
        fields = ['name', 'email', 'phone', 'message']
        extra_kwargs = {
            'phone': { 'optional': True }
        }
    
    def validate_email(self, value):
        return validate_email(value)
    
    def validate_phone(self, value):
        return re.match(r"^\\+?[1-9][0-9]{7,14}$", value)

class ComplaintListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaints
        fields = '__all__'