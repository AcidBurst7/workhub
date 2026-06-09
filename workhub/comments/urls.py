from django.urls import path
from .views import search_comments, search_comments_only, search_comments_in_requests, search_comments_in_requests_only

app_name = 'comments'

urlpatterns = [
    path('search_comments/', search_comments, name='search_comments'),
    path('search_comments_only/', search_comments_only, name='search_comments_only'),
    path('search_comments_in_requests/', search_comments_in_requests, name='search_comments_in_requests'),
    path('search_comments_in_requests_only/', search_comments_in_requests_only, name='search_comments_in_requests_only'),
]