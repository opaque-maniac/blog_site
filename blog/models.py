from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Model for individual post
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()
    cover_image = models.ImageField(upload_to='post_cover/', null=True, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    likes = models.PositiveBigIntegerField(default=0)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
    
    def __str__(self):
        return f'{self.title} by {self.author.email}'

# Model for comments
class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    likes = models.PositiveBigIntegerField(default=0)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
    
    def __str__(self):
        return f'{self.id} : {self.post.id} {self.author.id}'
    
# Model for favorites
class Favorite(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'favorite'
        verbose_name_plural = 'favorites'
    
    def __str__(self):
        return f'{ self.user.id } : { self.post.title }'

# Model for liked items
class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'content_id')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'liked item'
        verbose_name_plural = 'liked items'
    
    def __str__(self):
        return f'{ self.user.id } : { self.content_object.content[:5] }'

# Model for the notifications
class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type' ,'content_id')
    notification_content = models.CharField(max_length=250, blank=True, null=True)
    viewed = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'
    
    def __str__(self):
        return f'{ self.user.id } : { self.content_object.content[:5] }'
