from django.contrib import admin
from django.urls import path, include
import blog.views

urlpatterns = [
    path('home', blog.views.home, name='posthome'),
    path('post/<int:post_id>', blog.views.detail, name='detail'),
    path('post/new', blog.views.new, name='new'),
    path('post/<int:post_id>/edit', blog.views.edit, name='edit'),
    path('post/<int:post_id>/remove', blog.views.remove, name='remove'),
    path('post/<int:post_id>/newcomment', blog.views.newcomment, name='newcomment'),
    path('comment/<int:comment_id>/remove', blog.views.removecomment, name='removecomment'),
]