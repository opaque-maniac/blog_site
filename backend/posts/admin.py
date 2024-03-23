from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'author__first_name', 'author__last_name']
    list_display = ['title', 'author', 'date_created', 'date_updated']

class CommentAdmin(admin.ModelAdmin):
    search_fields = ['content', 'author__first_name', 'author__last_name']
    list_display = ['content', 'author', 'date_created', 'date_updated']

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)