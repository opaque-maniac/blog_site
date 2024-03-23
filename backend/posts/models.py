from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Model for post
class Post(models.Model):
    title = models.CharField(max_length=225)
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    cover_image = models.ImageField(upload_to='cover_images/', null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    class Meta:
        verbose_name=_('post')
        verbose_name_plural=_('posts')

    def __str__(self):
        return f'{ self.id } -> { self.title } -> { self.author.first_name }'

# Model for comments
class Comment(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=225)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    
    class Meta:
        verbose_name=_('post')
        verbose_name_plural=_('posts')

    def __str__(self):
        return f'{ self.id } -> { self.post.id } -> { self.author.first_name }'
