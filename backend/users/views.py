from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .permissions import IsOwner

# Register API
class RegisterAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

# Login API
class LoginAPIView(APIView):    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user': UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        return [permissions.AllowAny()]

# Profile API
class ProfileAPIView(APIView):
    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    
    def put(self, request):
        user = request.user
        serializer = UserSerializer(instance=user, data=request.body, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({
            'message': 'User deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAuthenticated(), IsOwner()]
        return [permissions.AllowAny()]
    
# Other users API
class ProfileDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return get_object_or_404(get_user_model(), id=self.kwargs['pk'])
    
    def get_permissions(self):
        return [permissions.IsAuthenticated(), IsOwner()]
