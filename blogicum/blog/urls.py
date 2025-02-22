from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # posts
    path(
        'posts/<int:id>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'posts/create/',
        views.create_post,
        name='create_post'
    ),
    path(
        'posts/<int:post_id>/edit/',
        views.edit_post,
        name='edit_post'
    ),
    path(
        'posts/<int:post_id>/delete/',
        views.delete_post,
        name='delete_post'
    ),
    # post comments
    path(
        'posts/<int:post_id>/comment/',
        views.add_comment,
        name='add_comment'),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        views.edit_comment,
        name='edit_comment',
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        views.delete_comment,
        name='delete_comment',
    ),
    # categories
    path(
        'category/<slug:category_slug>/',
        views.CategoryPostsView.as_view(),
        name='category_posts'
    ),
    # user profile
    path(
        'profile/edit/',
        views.edit_profile,
        name='edit_profile'),
    path(
        'profile/<str:username>/',
        views.profile_detail,
        name='profile'
    ),
    # index
    path(
        '',
        views.IndexView.as_view(),
        name='index'
    ),
]
