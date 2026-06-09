from django.urls import path
from .views import search_reminders, \
                    search_reminders_only, \
                    search_reminders_by_requests, \
                    search_reminders_by_requests_only
# 
app_name = 'reminders'

urlpatterns = [
    path('search_reminders/', search_reminders, name='search_reminders'),
    path('search_reminders_only/', search_reminders_only, name='search_reminders_only'),
    path('search_reminders_by_requests/', search_reminders_by_requests, name='search_reminders_by_requests'),
    path('search_reminders_by_requests_only/', search_reminders_by_requests_only, name='search_reminders_by_requests_only'),
]