from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
import json

from .views import get_next_posts
from .models import (
    Post,
    Comment,
    Favorite,
    Like,
    Notification
)
from .forms import (
    CommentForm,
    PostForm
)


"""
    Test the blog post model
    Test create method
    Test the string represantation
"""
class TestBlogPostModel(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()
    
    def test_create(self):
        self.assertEqual(self.post.title, self.post_details['title'])
        self.assertEqual(self.post.content, self.post_details['content'])
        self.assertEqual(self.post.author, self.post_details['author'])
        self.assertEqual(self.post.likes, 0)

    def test_string_representation(self):
        test_str = f'{self.post.title} by {self.post.author.email}'
        self.assertEqual(self.post.__str__(), test_str)
    
    def tearDown(self) -> None:
        self.user.delete()
        self.post.delete()


"""
    Test the comment model
    Test create method
    Test the string represantation
"""
class TestCommentModel(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()

        self.comment_details = {
            'author': self.user,
            'content': 'Nice description',
            'post': self.post,
        }
        self.comment = Comment.objects.create(**self.comment_details)
    
    def test_string_representation(self):
        expected = f"{self.comment.id} : {self.post.id} {self.comment.author.id}"
        self.assertEqual(self.comment.__str__(), expected)
    
    def test_create(self):
        self.assertEqual(self.comment.content, self.comment_details['content'])
        self.assertEqual(self.comment.author, self.comment_details['author'])
        self.assertEqual(self.comment.post, self.comment_details['post'])

    def tearDown(self) -> None:
        self.comment.delete()
        self.post.delete()
        self.user.delete()


"""
    Test the favorites model
    Test create method
    Test the string represantation
"""
class TestFavoritesModel(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()

        self.favorite_details = {
            'user': self.user,
            'post': self.post,
        }
        self.favorite = Favorite.objects.create(**self.favorite_details)

    def test_string_representation(self):
        string = f"{ self.user.id } : { self.post_details['title'] }"
        self.assertEqual(self.favorite.__str__(), string)
    
    def test_create_method(self):
        self.assertEqual(self.favorite.user, self.user)
        self.assertEqual(self.favorite.post, self.post)
    
    def tearDown(self) -> None:
        self.favorite.delete()
        self.post.delete()
        self.user.delete()


"""
    Test the liked model
    Test create method
    Test the string represantation
"""
class TestLikedModel(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()

        self.comment_details = {
            'author': self.user,
            'content': 'Nice description',
            'post': self.post,
        }
        self.comment = Comment.objects.create(**self.comment_details)
        self.comment.save()
    
        self.liked_post_details = {
            'user': self.user,
            'content_type': ContentType.objects.get_for_model(Post),
            'content_id': self.post.id,
            'content_object': self.post,
        }
        self.liked_post = Like.objects.create(**self.liked_post_details)
        self.liked_post.save()

        self.liked_comment_details = {
            'user': self.user,
            'content_type': ContentType.objects.get_for_model(Comment),
            'content_id': self.comment.id,
            'content_object': self.comment,
        }
        self.liked_comment = Like.objects.create(**self.liked_comment_details)
        self.liked_comment.save()
    
    def test_string_representation(self):
        self.assertEqual(self.liked_post.__str__(), f'{ self.user.id } : { self.post.content[:5] }')
        self.assertEqual(self.liked_comment.__str__(), f'{ self.user.id } : { self.comment.content[:5] }')

    def test_create_method(self):
        # For the liked post
        self.assertEqual(self.liked_post.content_object, self.post)
        self.assertEqual(self.liked_post.content_id, self.post.id)
        self.assertEqual(self.liked_post.user, self.user)    
        # For the liked comment
        self.assertEqual(self.liked_comment.content_object, self.comment)
        self.assertEqual(self.liked_comment.content_id, self.comment.id)
        self.assertEqual(self.liked_comment.user, self.user)

    def tearDown(self) -> None:
        self.liked_comment.delete()
        self.liked_post.delete()
        self.comment.delete()
        self.post.delete()
        self.user.delete()


"""
    Test the notification model
    Test create method
    Test the string represantation
"""
class TestNotificationModel(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()

        self.comment_details = {
            'author': self.user,
            'content': 'Nice description',
            'post': self.post,
        }
        self.comment = Comment.objects.create(**self.comment_details)
        self.comment.save()
    
        self.post_notification_details = {
            'user': self.user,
            'content_type': ContentType.objects.get_for_model(Post),
            'content_id': self.post.id,
            'content_object': self.post,
        }
        self.post_notification = Notification.objects.create(**self.post_notification_details)
        self.post_notification.save()

        self.comment_notification_details = {
            'user': self.user,
            'content_type': ContentType.objects.get_for_model(Comment),
            'content_id': self.comment.id,
            'content_object': self.comment,
        }
        self.comment_notification = Notification.objects.create(**self.comment_notification_details)
        self.comment_notification.save()
    
    def test_string_representation(self):
        self.assertEqual(self.post_notification.__str__(), f'{ self.user.id } : { self.post.content[:5] }')
        self.assertEqual(self.comment_notification.__str__(), f'{ self.user.id } : { self.comment.content[:5] }')

    def test_create_method(self):
        # For the post notification
        self.assertEqual(self.post_notification.content_object, self.post)
        self.assertEqual(self.post_notification.content_id, self.post.id)
        self.assertEqual(self.post_notification.user, self.user)
        self.assertFalse(self.post_notification.viewed)
        # For the comment notification
        self.assertEqual(self.comment_notification.content_object, self.comment)
        self.assertEqual(self.comment_notification.content_id, self.comment.id)
        self.assertEqual(self.comment_notification.user, self.user)
        self.assertFalse(self.post_notification.viewed)

    def tearDown(self) -> None:
        self.comment_notification.delete()
        self.post_notification.delete()
        self.comment.delete()
        self.post.delete()
        self.user.delete()


"""
    Test the all posts page view
    Test the response code => 302/200
    Test template used => 'blog/all_posts.html'
"""
class TestAllPostsView(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

    def test_response_code(self):
        response = self.client.get('/blog/posts/all/')
        self.assertEqual(response.status_code, 302)
    
    def test_reponse_code_name(self):
        resposne = self.client.get(reverse('blog:all_posts'))
        self.assertEqual(resposne.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:all_posts'))
        self.assertRedirects(response, f'/users/login/?next=/blog/posts/all/')
    
    def test_response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:all_posts'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:all_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/all_posts.html')
    
    def tearDown(self) -> None:
        self.user.delete()


"""
    Test the get next post view
    Test the response code => 302/200
    Test template used => None
    Test the json response
"""
class TestGetNexPost(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()
    
    def test_response_code(self):
        response = self.client.get('/blog/posts/next/')
        self.assertEqual(response.status_code ,302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:get_next_posts'))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:get_next_posts'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/blog/posts/next/')
    
    def test_response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:get_next_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
    
    def test_json_response(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:get_next_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse through the json response
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Found post(s)')
        self.assertIsNone(data['error_code'])
        # Check the author
        author = data['post_data'][0]['author']
        self.assertEqual(author['id'], self.user.id)
        self.assertEqual(author['first_name'], self.user.first_name)
        self.assertEqual(author['last_name'], self.user.last_name)
        # Check the post
        post = data['post_data'][0]
        self.assertEqual(post['id'], self.post.id)
        self.assertEqual(post['title'], self.post.title)
        self.assertFalse(post['liked'])

    def tearDown(self) -> None:
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:get_next_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

"""
    Test the individual post page
    Test response code => 302/200
    Test the template used => 'blog/individual_post.html'
    Test post method
"""
class TestIndividualPost(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()
    
    def test_response_code(self):
        reponse = self.client.get(f'/blog/posts/{ self.post.id }/')
        self.assertEqual(reponse.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:individual_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:individual_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next=/blog/posts/{ self.post.id }/')
    
    def test_reponse_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:individual_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:individual_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/individual_post.html')
    
    def tearDown(self) -> None:
        self.post.delete()
        self.user.delete()
    

"""
    Test the add to test the retrieve comments view
    Test the response code => 302/200
    Test template used => None
    Test json respnse
"""
class TestRetrieveComments(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()

        self.comment_details = {
            'author': self.user,
            'content': 'Nice description',
            'post': self.post,
        }
        self.comment = Comment.objects.create(**self.comment_details)
        self.comment.save()
    
    def test_response_code(self):
        response = self.client.get(f'/blog/posts/{ self.post.id }/comments/retrieve/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:retrieve_comments', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:retrieve_comments', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next=/blog/posts/{ self.post.id }/comments/retrieve/')
    
    def response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:retrieve_comments', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
    
    def test_json_response(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:retrieve_comments', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse json response
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIsNone(data['error_code'])
        self.assertIsNotNone(data['comment_data'])
        # Parse through comment data
        comment_data = data['comment_data'][0]
        self.assertEqual(comment_data['id'], self.comment.id)
        self.assertEqual(comment_data['content'], self.comment.content)
        # Parse through author data
        author_data = comment_data['author']
        self.assertEqual(author_data['id'], self.user.id)
        self.assertEqual(author_data['first_name'], self.user.first_name)
        self.assertEqual(author_data['last_name'], self.user.last_name)

    def tearDown(self) -> None:
        self.comment.delete()
        self.post.delete()
        self.user.delete()


"""
    Test the like post view
    Test the response code => 302/200
    Test template used => None
    Test the json response
"""
class TestLikePostView(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()
    
    def test_response_code(self):
        response = self.client.get(f'/blog/posts/{ self.post.id }/like/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:like_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:like_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next=/blog/posts/{ self.post.id }/like/')
    
    def test_response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:like_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_json_response(self):
        likes = Post.objects.get(id=self.post.id).likes
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:like_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse json response
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Thumbs up added')
        self.assertEqual(data['new_likes'], likes + 1)
        
    def test_invalid_json_response(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:like_post', args=[self.post.id + 2]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse through data
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Post does not exist')
        self.assertEqual(data['error_code'], '002')

    def tearDown(self) -> None:
        self.post.delete()
        self.user.delete()


"""
    Test the dislike post view
    Test the response code => 302/200
    Test template used => None
    Test the json response
"""
class TestDislikePostView(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()

        self.like_details = {
            'user': self.user,
            'content_id': self.post.id,
            'content_object': self.post,
            'content_type': ContentType.objects.get_for_model(Post)
        }
        self.like = Like.objects.create(**self.like_details)
        self.like.save()
    
    def test_response_code(self):
        response = self.client.get(f'/blog/posts/{ self.post.id }/dislike/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:dislike_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:dislike_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next=/blog/posts/{ self.post.id }/dislike/')
    
    def test_response_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:dislike_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse through json response
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIsNone(data['error_code'])
        self.assertEqual(data['message'], 'Thumbs up removed')
        # second response
        response = self.client.get(reverse('blog:dislike_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse through json response
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['error_code'], '002')
        self.assertEqual(data['message'], 'You have not liked this post')
    
    def test_invalid_json_response(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:dislike_post', args=[self.post.id + 1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse through json response
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Post does not exist')
        self.assertEqual(data['error_code'], '002')
    
    def tearDown(self) -> None:
        self.like.delete()
        self.post.delete()
        self.user.delete()


"""
    Test the edit post page
    Test response code => 302/200
    Test the template used => 'blog/edit_post.html'
    Test post method
"""
class TestEditPostView(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()
    
    def test_repsonse_code(self):
        response = self.client.get(f'/blog/posts/{ self.post.id }/edit/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:edit_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:edit_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next=/blog/posts/{ self.post.id }/edit/')
    
    def test_response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:edit_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:edit_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/edit_post.html')
    
    def tearDown(self) -> None:
        self.post.delete()
        self.user.delete()
    

"""
    Test the delete post view
    Test response code => 302/200
    Test the template used => None
"""
class TestDeletePost(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()

    def test_response_code(self):
        repsonse = self.client.get(f'/blog/posts/{ self.post.id }/delete/')
        self.assertEqual(repsonse.status_code, 302)
    
    def test_repsonse_code_name(self):
        response = self.client.get(reverse('blog:delete_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:delete_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next=/blog/posts/{ self.post.id }/delete/')
    
    def test_repsonse_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:delete_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog:all_posts'))
    
    def tearDown(self) -> None:
        self.post.delete()
        self.user.delete()


"""
    Test the favorites page
    Test response code => 302/200
    Test the template used => 'blog/favorites.html'
"""
class TestFavoritesPageView(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()
    
    def test_response_code(self):
        response = self.client.get('/blog/favorites/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:favorites'))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:favorites'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/blog/favorites/')
    
    def test_response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:favorites'))
        self.assertEqual(response.status_code, 200)
    
    def test_tempate_used(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/favorites.html')
    
    def tearDown(self) -> None:
        self.user.delete()


"""
    Test the retrieve favorites view
    Test the response code => 302/200
    Test template used => None
    Test the json response
"""
class TestRetrieveFavorites(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()

        self.favorite_details = {
            'user': self.user,
            'post': self.post,
        }
        self.favorite = Favorite.objects.create(**self.favorite_details)
        self.favorite.save()
    
    def test_response_code(self):
        response = self.client.get('/blog/favorites/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:favorites'))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:favorites'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/blog/favorites/')
    
    def response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password '])
        response = self.client.get(reverse('blog:retrieve_favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_json_response(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:retrieve_favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse json response
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIsNone(data['error_code'])
        # Parse favorites data
        favorites = data['post_data'][0]
        self.assertEqual(favorites['id'], self.post.id)
        self.assertEqual(favorites['title'], self.post.title)
    
    def tearDown(self) -> None:
        self.favorite.delete()
        self.post.delete()
        self.user.delete()


"""
    Test the add to favorites view
    Test the response code => 302/200
    Test template used => None
    Test the json response
"""
class TestAddToFavorites(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()
    
    def test_response_code(self):
        response = self.client.get(f'/blog/favorites/add/{ self.post.id }/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:add_to_favorites', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:add_to_favorites', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
    
    def test_response_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:add_to_favorites', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse json response
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Post added to favorites')
        self.assertIsNone(data['error_code'])
    
    def test_invalid_json_repsonse(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:add_to_favorites', args=[self.post.id + 1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse json response
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIsNotNone(data['error_code'])
    
    def tearDown(self) -> None:
        self.post.delete()
        self.user.delete()


"""
    Test the create comment view
    Test the response code => 302/200
    Test template used => None
    Test the json response
"""
class TestCreateCommentView(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()
    
    def test_response_code(self):
        response = self.client.get(f'/blog/posts/{ self.post.id }/comments/create/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:create_comment', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:create_comment', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next=/blog/posts/{ self.post.id }/comments/create/')
    
    def test_get_request(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:create_comment', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse json response
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIsNotNone(data['error_code'])
        self.assertEqual(data['error_code'], '005')
    
    def test_post_method(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.post(reverse('blog:create_comment', args=[self.post.id]), data={ 'content': 'Nice post' })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse json response
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIsNone(data['error_code'])
    
    def tearDown(self) -> None:
        self.post.delete()
        self.user.delete()


"""
    Test the edit comment view
    Test the response code => 302/200
    Test template used => None
    Test the json response
"""
class TestEditComment(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()

        self.comment_details = {
            'author': self.user,
            'content': 'Nice post',
            'post': self.post,
        }
        self.comment = Comment.objects.create(**self.comment_details)
        self.comment.save()
    
    def test_response_code(self):
        response = self.client.get(f'/blog/posts/comments/{ self.comment.id }/edit/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:edit_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 302)

    def test_redirect(self):
        response = self.client.get(reverse('blog:edit_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next=/blog/posts/comments/{ self.comment.id }/edit/')
    
    def test_get_response(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:edit_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse through json response
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIsNotNone(data['error_code'])
        self.assertEqual(data['error_code'], '005')
    
    def test_post_response(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.post(reverse('blog:edit_comment', args=[self.comment.id]), {
            'content': 'I expected better'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse through json response
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIsNone(data['error_code'])
    
    def test_invalid_json_response(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.post(reverse('blog:edit_comment', args=[self.comment.id + 2]), {
            'content': 'I expected better'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse through json response
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIsNotNone(data['error_code'])
    
    def tearDown(self) -> None:
        self.comment.delete()
        self.post.delete()
        self.user.delete()


"""
    Test the delete comment view
    Test the response code => 302/200
    Test template used => None
    Test the json response
"""
class TestDeleteComment(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()

        self.comment_details = {
            'author': self.user,
            'content': 'Nice post',
            'post': self.post,
        }
        self.comment = Comment.objects.create(**self.comment_details)
        self.comment.save()
    
    def test_response_code(self):
        response = self.client.get(f'/blog/posts/comments/{ self.comment.id }/delete/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:delete_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:delete_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next=/blog/posts/comments/{ self.comment.id }/delete/')
    
    def test_get_response(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:delete_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse json response
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIsNotNone(data['error_code'])
        self.assertEqual(data['error_code'], '005')
    
    def test_post_response(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.post(reverse('blog:delete_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse json response
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIsNone(data['error_code'])

    def tearDown(self) -> None:
        self.comment.delete()
        self.post.delete()
        self.user.delete()


"""
    Test the like comment view
    Test the response code => 302/200
    Test template used => None
    Test the json response
"""
class TestLikeComment(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()

        self.comment_details = {
            'author': self.user,
            'content': 'Nice post',
            'post': self.post,
        }
        self.comment = Comment.objects.create(**self.comment_details)
        self.comment.save()
    
    def test_response_code(self):
        response = self.client.get(f'/blog/posts/comments/{ self.comment.id }/like/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_authenticated(self):
        response = self.client.get(reverse('blog:like_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:like_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next=/blog/posts/comments/{ self.comment.id }/like/')
    
    def test_json_response(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:like_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse json response
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIsNone(data['error_code'])
    
    def test_invalid_json_response(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:like_comment', args=[self.comment.id + 1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse json response
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIsNotNone(data['error_code'])        

    def tearDown(self) -> None:
        self.comment.delete()
        self.post.delete()
        self.user.delete()


"""
    Test the like comment view
    Test the response code => 302/200
    Test template used => None
    Test the json response
"""
class TestDislikeComment(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()

        self.comment_details = {
            'author': self.user,
            'content': 'Nice post',
            'post': self.post,
        }
        self.comment = Comment.objects.create(**self.comment_details)
        self.comment.save()

        self.like_details = {
            'user': self.user,
            'content_id': self.comment.id,
            'content_type': ContentType.objects.get_for_model(Comment),
            'content_object': self.comment
        }
        self.like = Like.objects.create(**self.like_details)
        self.like.save()
    
    def test_response_code(self):
        response = self.client.get(f'/blog/posts/comments/{ self.comment.id }/dislike/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:dislike_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:dislike_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/login/?next=/blog/posts/comments/{ self.comment.id }/dislike/')
    
    def test_json_response(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:dislike_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse json response
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIsNone(data['error_code'])
        self.assertEqual(data['message'], 'Disliked comment')
    
    def test_invalid_json_response(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:dislike_comment', args=[self.comment.id + 2]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse json response
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertIsNotNone(data['error_code'])

    def tearDown(self) -> None:
        self.comment.delete()
        self.post.delete()
        self.user.delete()


"""
    Test the add to test the general liked page view
    Test the response code => 302/200
    Test template used => 'blog/liked.html'
"""
class TestLikedPage(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()
    
    def test_response_code(self):
        response = self.client.get('/blog/liked/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:liked'))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:liked'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/blog/liked/')
    
    def response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:liked'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:liked'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/liked.html')
    
    def tearDown(self) -> None:
        self.user.delete()
    

"""
    Test the add to test the liked posts page view
    Test the response code => 302/200
    Test template used => 'blog/liked_posts.html'
"""
class TestLikedPostPage(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()
    
    def test_response_code(self):
        response = self.client.get('/blog/liked/posts/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:liked_posts'))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:liked_posts'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/blog/liked/posts/')
    
    def response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:liked_posts'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:liked_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/liked_posts.html')
    
    def tearDown(self) -> None:
        self.user.delete()


"""
    Test the add to test the retrieve liked posts view
    Test the response code => 302/200
    Test template used => None
    Test json respnse
"""
class TestRetrieveLikedPosts(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()

        self.like_details = {
            'user': self.user,
            'content_id': self.post.id,
            'content_type': ContentType.objects.get_for_model(Post),
            'content_object': self.post
        }
        self.like = Like.objects.create(**self.like_details)
        self.like.save()
    
    def test_response_code(self):
        response = self.client.get('/blog/liked/posts/retrieve/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:retrieve_liked_posts'))
        self.assertEqual(response.status_code, 302)

    def test_redirect(self):
        response = self.client.get(reverse('blog:retrieve_liked_posts'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/blog/liked/posts/retrieve/')
    
    def response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:retrieve_liked_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
    
    def test_json_response(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:retrieve_liked_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse json response
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIsNone(data['error_code'])
        self.assertIsNotNone(data['post_data'])
        # Parse through post data
        post = data['post_data'][0]
        self.assertEqual(post['id'], self.post.id)
        self.assertEqual(post['title'], self.post.title)
        # Parse through author data
        author_data = post['author']
        self.assertEqual(author_data['id'], self.user.id)
        self.assertEqual(author_data['first_name'], self.user.first_name)
        self.assertEqual(author_data['last_name'], self.user.last_name)
    
    def tearDown(self) -> None:
        self.like.delete()
        self.post.delete()
        self.user.delete()


"""
    Test the add to test the liked comments page view
    Test the response code => 302/200
    Test template used => 'blog/liked_comments.html'
"""
class TestLikedCommentsPage(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()
    
    def test_response_code(self):
        response = self.client.get('/blog/liked/comments/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:liked_comments'))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:liked_comments'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/blog/liked/comments/')
    
    def response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:liked_comments'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:liked_comments'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/liked_comments.html')
    
    def tearDown(self) -> None:
        self.user.delete()


"""
    Test the retrieve comments view
    Test the response code => 302/200
    Test template used => None
    Test json response
"""
class TestRetrieveComments(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()

        self.comment_details = {
            'author': self.user,
            'content': 'Nice description',
            'post': self.post,
        }
        self.comment = Comment.objects.create(**self.comment_details)
        self.comment.save()
    
        self.liked_comment = {
            'user': self.user,
            'content_id': self.comment.id,
            'content_type': ContentType.objects.get_for_model(Comment),
            'content_object': self.comment
        }
        self.like = Like.objects.create(**self.liked_comment)
        self.like.save()
    
    def test_response_code(self):
        response = self.client.get('/blog/liked/comments/retrieve/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:retrieve_liked_comments'))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:retrieve_liked_comments'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/blog/liked/comments/retrieve/')
    
    def response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:retrieve_liked_comments'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
    
    def test_json_response(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:retrieve_liked_comments'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse json response
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIsNone(data['error_code'])
        self.assertIsNotNone(data['comment_data'])
        # Parse through comment data
        comment_data = data['comment_data'][0]
        self.assertEqual(comment_data['id'], self.comment.id)
        self.assertEqual(comment_data['content'], self.comment.content)
        # Parse through author data
        author_data = comment_data['author']
        self.assertEqual(author_data['id'], self.user.id)
        self.assertEqual(author_data['first_name'], self.user.first_name)
        self.assertEqual(author_data['last_name'], self.user.last_name)
    
    def tearDown(self) -> None:
        self.like.delete()
        self.comment.delete()
        self.post.delete()
        self.user.delete()


"""
    Test the add to test the notifications page view
    Test the response code => 302/200
    Test template used => 'blog/notifications.html'
"""
class TestNotificationsPage(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()
    
    def test_response_code(self):
        response = self.client.get('/blog/notifications/')
        self.assertEqual(response.status_code, 302)
    
    def test_reponse_code_name(self):
        response = self.client.get(reverse('blog:notifications'))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:notifications'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/blog/notifications/')
    
    def response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:notifications'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/notifications.html')
    
    def tearDown(self) -> None:
        self.user.delete()


"""
    Test the add to test the retrieve new notifications view
    Test the response code => 302/200
    Test template used => None
    Test json respnse
"""
class TestRetrieveNewNotifications(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()

        self.comment_details = {
            'author': self.user,
            'content': 'Nice description',
            'post': self.post,
        }
        self.comment = Comment.objects.create(**self.comment_details)
        self.comment.save()
    
        self.post_notification_details = {
            'user': self.user,
            'content_type': ContentType.objects.get_for_model(Post),
            'content_id': self.post.id,
            'content_object': self.post,
        }
        self.post_notification = Notification.objects.create(**self.post_notification_details)
        self.post_notification.save()

        self.comment_notification_details = {
            'user': self.user,
            'content_type': ContentType.objects.get_for_model(Comment),
            'content_id': self.comment.id,
            'content_object': self.comment,
        }
        self.comment_notification = Notification.objects.create(**self.comment_notification_details)
        self.comment_notification.save()
    
    def test_response_code(self):
        response = self.client.get('/blog/notifications/retrieve/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:retrieve_new_notifications'))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:retrieve_new_notifications'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/blog/notifications/retrieve/')
    
    def response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:retrieve_new_notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
    
    def test_json_response(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:retrieve_new_notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse json response
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIsNone(data['error_code'])
        self.assertIsNotNone(data['notification_data'])
        # Parse through notification data
        comment_notification = data['notification_data'][0]
        self.assertEqual(comment_notification['id'], self.comment_notification.id)
        # Parse through comment notification data
        post_notification = data['notification_data'][1]
        self.assertEqual(post_notification['id'], self.post_notification.id)
    
    def test_viewed_json_response(self):
        Notification.objects.filter(id=self.comment_notification.id).update(viewed=True)
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:retrieve_new_notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse json response
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIsNone(data['error_code'])
        self.assertIsNotNone(data['notification_data'])
        # Parse through notification data
        post_notification = data['notification_data'][0]
        self.assertEqual(post_notification['id'], self.post_notification.id)
        self.assertFalse(post_notification['viewed'])

    def tearDown(self) -> None:
        self.post_notification.delete()
        self.comment_notification.delete()
        self.comment.delete()
        self.post.delete()
        self.user.delete()


"""
    Test the add to test the all notifications page view
    Test the response code => 302/200
    Test template used => 'blog/all_notifications.html'
"""
class TestAllNotificationsPage(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()
    
    def test_response_code(self):
        response = self.client.get('/blog/notifications/all/')
        self.assertEqual(response.status_code, 302)
    
    def test_reponse_code_name(self):
        response = self.client.get(reverse('blog:all_notifications'))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:all_notifications'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/blog/notifications/all/')
    
    def response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:all_notifications'))
        self.assertEqual(response.status_code, 200)
    
    def test_template_used(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:all_notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/all_notifications.html')
    
    def tearDown(self) -> None:
        self.user.delete()


"""
    Test the add to test the retrieve all notifications view
    Test the response code => 302/200
    Test template used => None
    Test json respnse
"""
class TestRetrieveAllNotifications(TestCase):
    def setUp(self) -> None:
        self.user_credentials = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpassword'
        }
        self.user = get_user_model().objects.create_user(**self.user_credentials)
        self.user.save()

        self.post_details = {
            'title': 'Test post',
            'content': 'Woo hoo, can you see me',
            'author': self.user,
        }
        self.post = Post.objects.create(**self.post_details)
        self.post.save()

        self.comment_details = {
            'author': self.user,
            'content': 'Nice description',
            'post': self.post,
        }
        self.comment = Comment.objects.create(**self.comment_details)
        self.comment.save()
    
        self.post_notification_details = {
            'user': self.user,
            'content_type': ContentType.objects.get_for_model(Post),
            'content_id': self.post.id,
            'content_object': self.post,
        }
        self.post_notification = Notification.objects.create(**self.post_notification_details)
        self.post_notification.save()

        self.comment_notification_details = {
            'user': self.user,
            'content_type': ContentType.objects.get_for_model(Comment),
            'content_id': self.comment.id,
            'content_object': self.comment,
            'viewed': True
        }
        self.comment_notification = Notification.objects.create(**self.comment_notification_details)
        self.comment_notification.save()
    
    def test_response_code(self):
        response = self.client.get('/blog/notifications/all/retrieve/')
        self.assertEqual(response.status_code, 302)
    
    def test_response_code_name(self):
        response = self.client.get(reverse('blog:retrieve_all_notifications'))
        self.assertEqual(response.status_code, 302)
    
    def test_redirect(self):
        response = self.client.get(reverse('blog:retrieve_all_notifications'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login/?next=/blog/notifications/all/retrieve/')
    
    def response_code_authenticated(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:retrieve_all_notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
    
    def test_json_response(self):
        self.client.login(email=self.user_credentials['email'], password=self.user_credentials['password'])
        response = self.client.get(reverse('blog:retrieve_all_notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # Parse json response
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIsNone(data['error_code'])
        self.assertIsNotNone(data['notification_data'])
        # Parse through notification data
        comment_notification = data['notification_data'][0]
        self.assertEqual(comment_notification['id'], self.comment_notification.id)
        # Parse through comment notification data
        post_notification = data['notification_data'][1]
        self.assertEqual(post_notification['id'], self.post_notification.id)
    
    def tearDown(self) -> None:
        self.post_notification.delete()
        self.comment_notification.delete()
        self.comment.delete()
        self.post.delete()
        self.user.delete()