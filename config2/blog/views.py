from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.
class BlogListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    #context_object_name = 'all_blogs_list'

@login_required
class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

@login_required   
class BlogCreateView(CreateView):
    model = Post
    template_name = 'blog/post_new.html'
    fields = ['title', 'author', 'body']

@login_required
class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_edit.html'
    fields = ['title', 'author', 'body']

@login_required
class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('home')