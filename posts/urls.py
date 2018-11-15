from django.urls import path

from categories.views import random_post
from .views import PostDetailView, SearchPosts, UserPostsListView, PostUpdateView, PostCreateView, PostDeleteView

app_name = 'posts'

urlpatterns = [
    path('category/<slug:category_slug>/post/<slug:slug>/', PostDetailView.as_view(), name='post'),
    path('my-posts/', UserPostsListView.as_view(), name='my_posts'),
    path('post/random/', random_post, name='post_random'),
    path('post/<slug:slug>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/add/', PostCreateView.as_view(), name='post_add'),
    path('search/', SearchPosts.as_view(), name='search'),
]
