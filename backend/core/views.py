from rest_framework import permissions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from posts.models import Post, Comment
from posts.paginators import PostPagination
from posts.serializers import PostReadSerializer, CommentReadSerializer

from .serializer import ComplaintCreateSerialzier

# View for creating a complaint
class CreateComplaintView(generics.CreateAPIView):
    serializer_class = ComplaintCreateSerialzier
    permission_classes = [permissions.AllowAny]

# The explore page
class ExploreView(APIView):
    def get(self, request):
        query = self.request.GET.get('query', None)
        if query:
            posts = Post.objects.filter(title__icontains=query)
            comments = Comment.objects.filter(content__icontains=query)
        else:
            posts = Post.objects.all()
            comments = Comment.objects.all()
        
        paginator = PostPagination()
        paginated_posts = paginator.paginate_queryset(posts, request)
        paginated_comments = paginator.paginate_queryset(comments, request)

        post_serializer = PostReadSerializer(paginated_posts, many=True)
        comment_serializer = CommentReadSerializer(paginated_comments, many=True)
        return Response({
            'posts': post_serializer.data,
            'comments': comment_serializer.data
        }, status=status.HTTP_200_OK)

    