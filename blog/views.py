from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers import serialize
from django.urls import reverse
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import EmptyResultSet, ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from .models import (
    Post,
    Comment,
    Favorite,
    Like,
    Notification
)
from .forms import PostForm, CommentForm


"""
    This is a view function for the all posts page
    It uses no forms
    It renders => 'blog/all_posts.html'
"""
@login_required
def all_posts(request):
    return render(request, 'blog/all_posts.html')


"""
    This is a view function to retrieve posts dynamically
    It uses the no forms
    It returns a json response
"""
@login_required
def get_next_posts(request):
    try:
        last_post_id = request.GET.get('last_post_id')

        if last_post_id:
            next_posts = Post.objects.filter(id__lt=last_post_id).order_by('-id')[:5]
        else:
            next_posts = Post.objects.all().order_by('-id')[:20]
            
        return JsonResponse({
            'success': True,
            'message': 'Found post(s)',
            'error_code': None,
            'post_data': [
                {
                    'id': post.id,
                    'title': post.title,
                    'url': reverse('blog:individual_post', args=[post.id]),
                    'author': {
                        'id': post.author.id,
                        'first_name': post.author.first_name,
                        'last_name': post.author.last_name,
                        'url': reverse('blog:user_profile', args=[post.author.id])
                    },
                    'liked': True if Like.objects.filter(content_id=post.id, user=request.user).exists() else False,
                } for post in next_posts
            ]
        })
    except EmptyResultSet:
        return JsonResponse({
            'success': False,
            'message': 'No post found',
            'error_code': '001'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error occured when retrieving posts',
            'error_code': '002',
            'error_message': f'{ e }'
        })


"""
    This is a view function for the all posts page
    It uses no forms
    It renders => 'blog/all_posts.html'
"""
@login_required
def individual_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    Post.objects.filter(id=post_id).update(views=F('views') + 1)
    form = CommentForm()
    return render(request, 'blog/individual_post.html', {
        'post': post,
        'form': form,
    })


"""
    This is a view function giving a post a thumbs up
    It uses no form
    It returns a json response
"""
@login_required
def like_post(request, post_id):
    try:
        like = Like.objects.filter(user=request.user, content_id=post_id).first()
        if like:
            return JsonResponse({
                'success': False,
                'message': 'You already liked this post',
                'error_code': '002'
            })
        post = Post.objects.get(id=post_id)
        Post.objects.filter(id=post_id).update(likes=F('likes') + 1)
        Like.objects.create(
            user=request.user,
            content_type=ContentType.objects.get_for_model(Post),
            content_id=post_id,
            content_object=post
        )
        Notification.objects.create(
            user=Post.objects.get(id=post_id).author,
            content_id=post_id,
            content_type=ContentType.objects.get_for_model(Post),
            content_object=post,
            notification_content=f'{ request.user.first_name } { request.user.last_name } liked your post'
        )
        return JsonResponse({
            'success': True,
            'message': 'Thumbs up added',
            'new_likes': Post.objects.get(id=post_id).likes,
            'error_code': None
        })
    except Post.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Post does not exist',
            'error_code': '002'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error occured when giving post a thumbs up',
            'error_code': '003'
        })


"""
    This is a view function for giving a post a thumbs down
    It uses no form
    It returns a json response
"""
@login_required
def dislike_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        like = Like.objects.filter(user=request.user, content_id=post_id).first()
        if like:
            if like.user != request.user:
                return JsonResponse({
                    'success': False,
                    'message': 'Permission denied',
                    'error_code': '006'
                })
            like.delete()
            if post.likes > 0:
                Post.objects.filter(id=post_id).update(likes=F('likes') - 1)            
            return JsonResponse({
                'success': True,
                'message': 'Thumbs up removed',
                'new_likes': Post.objects.get(id=post_id).likes,
                'error_code': None
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'You have not liked this post',
                'error_code': '002'
            })
    except Post.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Post does not exist',
            'error_code': '002'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error occurred while removing thumbs up',
            'error_code': '002',
            'error_message': str(e)
        })


"""
    This is a view function for the edit post page
    It uses Post Form
    It renders => 'blog/edit_post.html'
"""
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        raise Http404(_('Permission denied'))
    if request.method == 'POST':
        form = PostForm(instance=post, data=request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect(reverse('blog:individual_post', args=[post.id]))
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {
        'form': form,
        'post': post
    })


"""
    This is a view function for the delete post page
    It uses no form
    It renders => None
"""
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        raise Http404(_('Permission denied'))
    post.delete()
    return redirect(reverse('blog:all_posts'))


"""
    This is a view function for the favorites page
    It uses no forms
    It renders => 'blog/favorites.html'
"""
@login_required
def favotires(request):
    favorites_count = Favorite.objects.filter(user=request.user).count()
    return render(request, 'blog/favorites.html', {
        'favorite_count': favorites_count
    })


""" 
    This is a view function for retrieving favorites
    It uses no forms
    It returns a json response
"""
@login_required
def retrieve_favorite(request):
    try:
        last_post_id = request.GET.get('last_post_id')
        if last_post_id:
            favorites = Favorite.objects.filter(user=request.user, post__id__lt=last_post_id).order_by('-id')[:5]
        else:
            favorites = Favorite.objects.filter(user=request.user)[:20]
        return JsonResponse({
            'success': True,
            'message': 'Favorites retrieved',
            'error_code': None,
            'favorites': [
                {
                    'id': favorite.post.id,
                    'title': favorite.post.title,
                    'url': reverse('blog:individual_post', args=[favorite.post.id]),
                    'author': {
                        'id': favorite.post.author.id,
                        'first_name': favorite.post.author.first_name,
                        'last_name': favorite.post.author.last_name,
                        'url': reverse('blog:user_profile', args=[favorite.post.author.id])
                    },
                    'liked': True if Like.objects.filter(content_id=favorite.post.id, user=request.user).exists() else False,
                }
                for favorite in favorites
            ]
        })
    except Favorite.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'No favorite found',
            'error_code': '001'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error occured when retrieving favorites',
            'error_code': '002',
            'error_message': f'{ e }'
        })


"""
    This is a view function for adding favorites
    It uses no forms
    It returns a json response
"""
@login_required
def add_to_favorites(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        favorite = Favorite.objects.filter(user=request.user, post=post).first()
        if favorite:
            return JsonResponse({
                'success': False,
                'message': 'Post already in favorites',
                'error_code': '002'
            })
        Favorite.objects.create(user=request.user, post=post)
        return JsonResponse({
            'success': True,
            'message': 'Post added to favorites',
            'error_code': None
        })
    except Post.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Post does not exist',
            'error_code': '002'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error occured when adding to favorites',
            'error_code': '003',
            'error_message': f'{ e }'
        })


"""
    This is a view function for removing favorites
    It uses no forms
    It returns a json response
"""
@login_required
def remove_from_favorites(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        favorite = Favorite.objects.filter(user=request.user, post=post).first()
        if not favorite:
            return JsonResponse({
                'success': False,
                'message': 'Post not in favorites',
                'error_code': '002'
            })
        favorite.delete()
        return JsonResponse({
            'success': True,
            'message': 'Post removed from favorites',
            'error_code': None
        })
    except ObjectDoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Post does not exist',
            'error_code': '002'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error occured when removing from favorites',
            'error_code': '003',
            'error_message': f'{ e }'
        })
    

"""
    This is a view function for creating a comment
    It uses no forms
    It returns a json response
"""
@login_required
def create_comment(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                Notification.objects.create(
                    user=post.author,
                    content_id=post_id,
                    content_type=ContentType.objects.get_for_model(Post),
                    content_object=post,
                    notification_content=f'{ request.user.first_name } { request.user.last_name } commented on your post'
                )
                return JsonResponse({
                    'success': True,
                    'message': 'Comment added',
                    'error_code': None,
                    'comment': {
                        'id': comment.id,
                        'author': {
                            'id': comment.author.id,
                            'first_name': comment.author.first_name,
                            'last_name': comment.author.last_name
                        },
                        'content': comment.content,
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid form',
                    'error_code': '004'
                })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request method',
                'error_code': '005'
            })
    except Post.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Post does not exist',
            'error_code': '002'
    
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error occured when adding comment',
            'error_code': '003',
            'error_message': f'{ e }'
        })


"""
    This is a view function for editing a comment
    It uses no forms
    It returns a json response
"""
@login_required
def edit_comment(request, comment_id):
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.author != request.user:
            return JsonResponse({
                'success': False,
                'message': 'Permission denied',
                'error_code': '006'
            })
        if request.method == 'POST':
            form = CommentForm(data=request.POST)
            if form.is_valid():
                Comment.objects.filter(id=comment_id).update(content=form.cleaned_data['content'])
                return JsonResponse({
                    'success': True,
                    'message': 'Comment edited',
                    'error_code': None
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid form',
                    'error_code': '004'
                })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request method',
                'error_code': '005'
            })
    except ObjectDoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Comment does not exist',
            'error_code': '002'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error occured when editing comment',
            'error_code': '003',
            'error_message': f'{ e }'
        })


"""
    This is a view function for deleting a comment
    It uses no forms
    It returns a json response
"""
@login_required
def delete_comment(request, comment_id):
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.author != request.user:
            return JsonResponse({
                'success': False,
                'message': 'Permission denied',
                'error_code': '006'
            })
        if request.method == 'POST':
            Comment.objects.filter(id=comment_id).delete()
            return JsonResponse({
                'success': True,
                'message': 'Comment deleted',
                'error_code': None
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request method',
                'error_code': '005'
            })
    except ObjectDoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Comment does not exist',
            'error_code': '002'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error occured when deleting comment',
            'error_code': '003',
            'error_message': f'{ e }'
        })


"""
    This is a view function for liking a comment
    It uses no forms
    It returns a json response
"""
@login_required
def like_comment(request, comment_id):
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        Comment.objects.filter(id=comment_id).update(likes=F('likes') + 1)
        Like.objects.create(
            user=request.user,
            content_id=comment.id,
            content_object=comment,
            content_type=ContentType.objects.get_for_model(Comment)
        )
        Notification.objects.create(
            user=comment.author,
            content_id=comment.id,
            content_object=comment,
            content_type=ContentType.objects.get_for_model(Comment),
            notification_content=f'{ request.user.first_name } { request.user.last_name } liked your comment'
        )
        return JsonResponse({
            'success': True,
            'message': 'Liked comment',
            'error_code': None
        })
    except ObjectDoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Comment not found',
            'error_code': '002'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error occured when liking comment',
            'error_code': '003',
            'error_message': f'{ e }'
        })


"""
    This is a view function for disliking a comment
    It uses no forms
    It returns a json response
"""
@login_required
def dislike_comment(request, comment_id):
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        like = Like.objects.filter(user=request.user, content_id=comment_id).first()
        if like:
            if like.user != request.user:
                return JsonResponse({
                    'success': False,
                    'message': 'Permission denied',
                    'error_code': '006'
                })
            if comment.likes > 0:
                Comment.objects.filter(id=comment_id).update(likes=F('likes') - 1)
            return JsonResponse({
                'success': True,
                'message': 'Disliked comment',
                'error_code': None
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Like not found for this comment',
                'error_code': '002',
            })
    except ObjectDoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Comment not found',
            'error_code': '002'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error occured when disliking post',
            'error_code': '003',
            'error_message': f'{ e }'
        })


"""
    This is a view function for the liked object page
    It uses no form
    It renders => 'blog/liked.html'
"""
@login_required
def liked(request):
    return render(request, 'blog/liked.html')


"""
    This is a view function for the liked posts page
    It uses no form
    It renders => 'blog/liked.html'
"""
@login_required
def liked_posts(request):
    content_type = ContentType.objects.get_for_model(Post)
    liked_count = Like.objects.filter(user=request.user, content_type=content_type).count()
    return render(request, 'blog/liked_posts.html', {
        'count': liked_count
    })


"""
    This is a view function for retrieving liked posts
    It uses no forms
    It returns a json response
"""
@login_required
def retrieve_liked_posts(request):
    try:
        content_type = ContentType.objects.get_for_model(Post)
        last_post_id = request.GET.get('last_post_id')
        if last_post_id:
            liked = Like.objects.filter(
                user=request.user,
                content_type=content_type,
                content_id__lt=last_post_id
            ).order_by('-content_id')[:5]
        else:
            liked = Like.objects.filter(
                user=request.user,
                content_type=content_type
            ).order_by('-content-id')[:20]
        return JsonResponse({
            'success': True,
            'message': 'Retrieved liked posts',
            'error_code': None,
            'post_data': [
                {
                    'id': like.content_object.id,
                    'title': like.content_object.title,
                    'url': reverse('blog:individual_post', args=[like.content_id]),
                    'author': {
                        'id': like.content_object.author.id,
                        'first_name': like.content_object.author.first_name,
                        'last_name': like.content_object.author.last_name,
                        'url': reverse('blog:user_profile', args=[like.content_object.author.id])
                    }
                }
                for like in liked
            ]
        })
    except EmptyResultSet:
        return JsonResponse({
            'success': False,
            'message': 'No liked posts',
            'error_code': '001'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error occured when retrieving posts',
            'error_code': '003',
            'error_message': f'{ e }'
        })


"""
    This is a view function for the liked comments page
    It uses no form
    It renders => 'blog/liked.html'
"""
@login_required
def liked_comments(request):
    content_type = ContentType.objects.get_for_model(Comment)
    liked_count = Like.objects.filter(user=request.user, content_type=content_type).count()
    return render(request, 'blog/liked_comments.html', {
        'count': liked_count
    })


"""
    This is a view function for retrieving liked posts
    It uses no forms
    It returns a json response
"""
@login_required
def retrieve_liked_comments(request):
    try:
        content_type = ContentType.objects.get_for_model(Comment)
        last_post_id = request.GET.get('last_post_id')
        if last_post_id:
            liked = Like.objects.filter(
                user=request.user,
                content_type=content_type,
                content_id__lt=last_post_id
            ).order_by('-content_id')[:5]
        else:
            liked = Like.objects.filter(
                user=request.user,
                content_type=content_type
            ).order_by('-content-id')[:20]
        return JsonResponse({
            'success': True,
            'message': 'Retrieved liked comments',
            'error_code': None,
            'post_data': [
                {
                    'id': like.content_object.id,
                    'title': like.content_object.title,
                    'author': {
                        'id': like.content_object.author.id,
                        'first_name': like.content_object.author.first_name,
                        'last_name': like.content_object.author.last_name,
                        'url': reverse('blog:user_profile', args=[like.content_object.author.id])
                    }
                }
                for like in liked
            ]
        })
    except EmptyResultSet:
        return JsonResponse({
            'success': False,
            'message': 'No liked comments',
            'error_code': '001'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error occured when retrieving posts',
            'error_code': '003',
            'error_message': f'{ e }'
        })