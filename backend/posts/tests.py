from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Post, Comment

# Test Post model
class TestPostModel(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'thisismypassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)

        self.post_details = {
            'title': 'Test Post',
            'content': 'This is a test post',
            'author': self.user
        }
        self.post = Post.objects.create(**self.post_details)
    
    def test_post_content(self) -> None:
        self.assertEqual(self.post.title, self.post_details['title'])
        self.assertEqual(self.post.content, self.post_details['content'])
        self.assertEqual(self.post.author, self.post_details['author'])

    def tearDown(self) -> None:
        self.post.delete()
        self.user.delete()

class TestCommentModel(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'thisismypassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)

        self.post_details = {
            'title': 'Test Post',
            'content': 'This is a test post',
            'author': self.user
        }
        self.post = Post.objects.create(**self.post_details)

        self.comment_details = {
            'post': self.post,
            'author': self.user,
            'content': 'Nice post'
        }
        self.comment = Comment.objects.create(**self.comment_details)
    
    def test_comment_content(self) -> None:
        self.assertEqual(self.comment.post, self.comment_details['post'])
        self.assertEqual(self.comment.author, self.comment_details['author'])
        self.assertEqual(self.comment.content, self.comment_details['content'])

    def tearDown(self) -> None:
        self.comment.delete()
        self.post.delete()
        self.user.delete()