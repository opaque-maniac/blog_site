from django.urls import path
from .views import (
    all_posts,
    get_next_posts,
    individual_post,
    like_post,
    dislike_post,
    edit_post,
    delete_post,
    favotires,
    retrieve_favorite,
    add_to_favorites,
    remove_from_favorites,
    create_comment,
    edit_comment,
    delete_comment,
    like_comment,
    dislike_comment,
)

app_name = 'blog'

# URLs for the blog application
urlpatterns = [
    path('posts/all/', all_posts, name='all_posts'),
    path('posts/next/', get_next_posts, name='get_next_posts'),
    path('posts/<int:post_id>/', individual_post, name='individual_post'),
    path('posts/<int:post_id>/like/', like_post, name='like_post'),
    path('posts/<int:post_id>/dislike/', dislike_post, name='dislike_post'),
    path('posts/<int:post_id>/edit/', edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('favorites/', favotires, name='favorites'),
    path('favorites/retrieve/', retrieve_favorite, name='retrieve_favorites'),
    path('favorites/add/<int:post_id>/', add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:post_id>/', remove_from_favorites, name='remove_from_favorites'),
    path('posts/<int:post_id>/comments/create/', create_comment, name='create_comment'),
    path('posts/comments/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
    path('posts/comments/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('posts/comments/<int:comment_id>/like/', like_comment, name='like_comment'),
    path('posts/comments/<int:comment_id>/dislike/', dislike_comment, name='dislike_comment')
]
