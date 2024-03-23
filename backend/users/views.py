from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login

from .models import CustomUser
from .serializers import (
    UserReadSerializer,
    UserLoginSerializer,
    UserRegisrerSerializer,
    UserUpdateSerializer,
)

# View for registering users
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisrerSerializer
    permission_classes = [permissions.AllowAny]

# View for logging in users
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(email=email, password=password)
            login(user)
            return Response(UserUpdateSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for profile
class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    def get_object(self):
        user_id = self.kwargs.get('pk', None)
        user = get_object_or_404(CustomUser, id=user_id)
        return user
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return UserUpdateSerializer
        return UserReadSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), permissions.IsOwnerOrReadOnly()]
        return [permissions.AllowAny()]
    