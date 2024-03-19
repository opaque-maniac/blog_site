from rest_framework import serializers
from .models import Post, Comment

# Post serializers
# Post, POST, PUT serializer
class PostPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

# Post, GET serializer
class PostGETSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']

# Comment serializers
# Comment POST, PUT serializer
class CommentPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'post']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

# Comment GET serializer
class CommentGETSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'post', 'created_at', 'updated_at']