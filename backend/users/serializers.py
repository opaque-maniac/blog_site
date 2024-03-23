from rest_framework import serializers
from validate_email import validate_email

from .models import CustomUser

# Serializer for read
class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'profile_image']
    
    def validate_email(self, value):
        return validate_email(value)
    
# Serializer for registering a user
class UserRegisrerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }
    
    def validate_email(self, value):
        return validate_email(value)
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

# Serializer for logging in a user
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
    
    def validate_email(self, value):
        return validate_email(value)

# Serializer for updating user account information
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'email': {
                'read_only': True
            },
            'password': {
                'write_only': True,
                'required': False
            }
        }
    
    def validate_email(self, value):
        return validate_email(value)