from rest_framework import (
    generics,
    permissions,
    status,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import F

from .serializers import (
    PostReadSerializer,
    PostWriteSerializer,
    CommentReadSerializer, 
    CommentWriteSerializer,
)
from .permissions import IsAuthorOrReadOnly
from .models import Post, Comment
from .paginators import (
    PostPagination,
    CommentPaginaton,
)

# View for listing and creating new posts
# Supports GET, POST
class PostListView(generics.ListCreateAPIView):
    pagination_class = PostPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
	
    def get_serializer_classes(self):
        if self.request.method == 'GET':
            return PostReadSerializer
        return PostWriteSerializer
    
    def get_queryset(self):
        return Post.objects.all()

# View for post detial
# Supports GET, PUT, DELETE
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
	
    def get_serializer_classes(self):
        if self.request.method == 'GET':
            return PostReadSerializer
        return PostWriteSerializer
	
    def get_object(self):
        obj_id = self.kwargs.get('pk', None)
        post = get_object_or_404(Post.objects.select_for_updates().filter(pk=obj_id), id=obj_id)
        post.likes = F('views') + 1
        post.save(updated_fields=['views'])
        return post
		
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]
        return [permissions.IsAuthenticated()]

# View for liking posts and disliking posts
# Supports PUT, DELETE
class LikeAndDislikePost(APIView):
    def put(self, request, pk):
        post = get_object_or_404(Post.objects.select_for_updates().filter(pk=pk), id=pk)
        post.likes = F('likes') + 1
        post.save(updated_fields=['likes'])
        return Response(
			PostReadSerializer(post).data,
			status=status.HTTP_200_OK
		)
    
    def delete(self, request, pk):
        post = get_object_or_404(Post.objects.select_for_updates().filter(pk=pk), id=pk)
        post.likes = F('likes') - 1 if post.likes > 0 else 0
        post.save(updated_fields=['likes'])
        return Response(
			PostReadSerializer(post).data,
			status=status.HTTP_200_OK
		)
		
# View to list and create comments
class CommentListView(generics.ListCreateAPIView):
    pagination_class = CommentPaginaton

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['post'] = get_object_or_404(Post, pk=self.kwargs.get('pk', None))
        return context
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentReadSerializer
        return CommentWriteSerializer
    
    def get_queryset(self):
        post_id = self.kwargs.get('pk', None)
        return Comment.objects.filter(post=post_id)

# View for comment detail
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        context['post'] = get_object_or_404(Post, pk=self.kwargs.get('post_pk', None))
        return context
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentReadSerializer
        return CommentWriteSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]
    
    def get_object(self):
        obj_id = self.kwargs.get('pk', None)
        post_id = self.kwargs.get('post_pk', None)
        comment =  get_object_or_404(Comment.objects.select_for_update().filter(post=post_id), id=obj_id)
        comment.views = F('views') + 1
        comment.save(updated_fields=['views'])
        return comment

# View for liking and disliking a comment
class LikeAndDislikeComment(APIView):
    def put(self, request, post_pk, pk):
        comment = get_object_or_404(Comment.objects.select_for_update().filter(post=post_pk), id=pk)
        comment.likes = F('likes') + 1
        comment.save(updated_fields=['likes'])
        return Response(
            CommentReadSerializer(comment).data,
            status=status.HTTP_200_OK
        )
    
    def delete(self, request, post_pk, pk):
        comment = get_object_or_404(Comment.objects.select_for_update().filter(post=post_pk), id=pk)
        comment.likes = F('likes') - 1 if comment.likes > 0 else 0
        comment.save(updated_fields=['likes'])
        return Response(
            CommentReadSerializer(comment).data,
            status=status.HTTP_200_OK
        )