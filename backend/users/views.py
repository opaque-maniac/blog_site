from rest_framework import permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
)
from .permissions import IsOwnerOrReadOnly
from posts.serializers import PostReadSerializer
from posts.paginators import PostPagination
from posts.models import Post

# User model
User = get_user_model()

# View for the register page
class Registerview(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

# View for the login
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                email=serializer.validated_data.get('email'),
                password=serializer.validated_data.get('password')
            )
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user': UserProfileSerializer(user).data
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for the user profile
class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [IsOwnerOrReadOnly(), permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserProfileSerializer
        return UserUpdateSerializer
    
    def get_object(self):
        user_id = self.kwargs.get('pk', None)
        user = get_object_or_404(User, pk=user_id)
        return user

# View for a users posts
class UserPostsView(generics.ListAPIView):
    serializer_class = PostReadSerializer
    pagination_class = PostPagination

    def get_queryset(self):
        user_id = self.kwargs.get('pk', None)
        return Post.objects.filter(author__id=user_id)
