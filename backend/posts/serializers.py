from rest_framework import serializers

from .models import Post, Comment

# Post serializer for GET
class PostReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

# Post serialzier for creating and updating
class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'cover_image', 'author']
        extra_kwargs = {
            'cover_image': {
                'required': False
                },
            'author': {
                'required': False
            }
            }

    def create(self, validated_data):
        data = {
                **validated_data,
                'author': self.context['request'].user
                }
        return Post.objects.create(**data)

# Comment serializer for GET
class CommentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

# Comment serializer for creating and updating
class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'author', 'post']
        extra_kwargs = {
            'author': {
                'required': False
                }
            }

        def create(self, validated_data):
            data = {
                    **validated_data,
                    'author': self.context['request'].user,
                    'post': self.context['post']
            }
            return Comment.objects.create(**data)