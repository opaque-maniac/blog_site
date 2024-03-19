from rest_framework import permissions, generics
from django.shortcuts import get_object_or_404

from .models import Post, Comment
from .serializers import PostPOSTSerializer, PostGETSerializer, CommentPOSTSerializer, CommentGETSerializer
from .permissions import IsAuthorOrReadOnly

# View for listing all posts and creating a new post
class PostListView(generics.ListCreateAPIView):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        last_post_id = self.request.query_params.get('last_post_id', None)
        if last_post_id:
            posts = Post.objects.filter(id__lt=last_post_id).order_by('-id')[:10]
        else:
            posts = Post.objects.all().order_by('-id')[:10]
        return posts

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostPOSTSerializer
        return PostGETSerializer

# View for retrieving, updating and deleting a post
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_object(self):
        return get_object_or_404(Post, id=self.kwargs['pk'])
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return PostPOSTSerializer
        return PostGETSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]
        return [permissions.IsAuthenticated()]

# View for listing all comments and creating a new comment
class CommentListView(generics.ListCreateAPIView):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_queryset(self):
        post_id = self.request.query_params.get('post_id', None)
        post = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post=post).order_by('-id')
        return comments
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentPOSTSerializer
        return CommentGETSerializer
    
# View for retrieving, updating and deleting a comment
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs.get('pk'))
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return CommentPOSTSerializer
        return CommentGETSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]
        return [permissions.IsAuthenticated()]
