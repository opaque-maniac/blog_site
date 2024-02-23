from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Post, Comment

# Form for new post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'cover_image', 'content']
        labels = {
            'title': _('Title'),
            'conver_image': _('Cover Image'),
            'content': None
        }
        widgets = {
            'title': forms.TextInput(attrs={ 'autofocus': True }),
            'cover_image': forms.TextInput(attrs={ 'autofocus': False }),
        }

# Form for new comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={ 'autofocus': False, 'placeholder': 'Comment here...' })
        }