from django.urls import path

from .views import (
    PostListView,
    PostDetailView,
    LikeAndDislikePost,
    CommentListView,
    CommentDetailView,
    LikeAndDislikeComment,
)

app_name = 'posts'

# URLs for the posts application
urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', LikeAndDislikePost.as_view(), name='post-like'),
    path('posts/<int:pk>/comments/', CommentListView.as_view(), name='comment-list'),
    path('posts/<int:pk>/comments/<int:comment_pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('posts/<int:pk>/comments/<int:comment_pk>/like/', LikeAndDislikeComment.as_view(), name='comment-like'),
]
