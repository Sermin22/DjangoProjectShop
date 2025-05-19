from django.urls import path
from blog.apps import BlogConfig
from .views import (BlogPostListView,  BlogPostDetailView, BlogPostCreateView,
                    BlogPostUpdateView, BlogPostDeleteView)


app_name = BlogConfig.name

urlpatterns = [
    path('blogs/', BlogPostListView.as_view(), name='blogpost_list'),
    path('blogs/<int:pk>/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('blogs/create/', BlogPostCreateView.as_view(), name='blogpost_create'),
    path('blogs/<int:pk>/update/', BlogPostUpdateView.as_view(), name='blogpost_update'),
    path('blogs/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blogpost_delete'),
]