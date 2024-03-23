from rest_framework import (
    generics,
    permissions,
    status,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import F

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
	
    def get_serializer_class(self):
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
	
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostReadSerializer
        return PostWriteSerializer
	
    def get_object(self):
        obj_id = self.kwargs.get('pk', None)
        Post.objects.filter(pk=obj_id).update(views=F('views') + 1)
        post = get_object_or_404(Post, pk=obj_id)
        return post
		
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]
        

# View for liking posts and disliking posts
# Supports PUT, DELETE
class LikeAndDislikePost(APIView):
    def put(self, request, pk):
        Post.objects.filter(pk=pk).update(likes=F('likes') + 1)
        post = get_object_or_404(Post, pk=pk)
        return Response(
			PostReadSerializer(post).data,
			status=status.HTTP_200_OK
		)
    
    def delete(self, request, pk):
        Post.objects.filter(pk=pk).update(likes=F('likes') - 1 if F('likes') > 0 else 0)
        post = get_object_or_404(Post, pk=pk)
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
        context['post'] = get_object_or_404(Post, pk=self.kwargs.get('pk', None))
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentReadSerializer
        return CommentWriteSerializer
    
    def get_object(self):
        post_id = self.kwargs.get('pk', None)
        comment_id = self.kwargs.get('comment_pk', None)
        Comment.objects.filter(post=post_id, pk=comment_id).update(views=F('views') + 1)
        comment = get_object_or_404(Comment, pk=comment_id)
        return comment
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]

# View for liking and disliking a comment
class LikeAndDislikeComment(APIView):
    def put(self, request, pk, comment_pk):
        Comment.objects.filter(post=pk, id=comment_pk).update(likes=F('likes') + 1)
        comment = get_object_or_404(Comment, comment_pk=pk)
        return Response(
            CommentReadSerializer(comment).data,
            status=status.HTTP_200_OK
        )
    
    def delete(self, request, post_pk, pk):
        Comment.objects.filter(post=post_pk, id=pk).update(likes=F('likes') - 1 if F('likes') > 0 else 0)
        comment = get_object_or_404(Comment, pk=pk)
        return Response(
            CommentReadSerializer(comment).data,
            status=status.HTTP_200_OK
        )