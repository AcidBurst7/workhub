from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    path('', views.index, name='index'),
    path('tasks/', views.tasks, name='tasks'),
    path('requests/', views.requests, name='requests'),
    path('calendar/', views.calendar, name='calendar'),
    path('search_request/', views.search_request, name='search_request'),
    path('tasks_pom/', views.tasks_pom, name='tasks_pom'),
    path('projects/', views.projects, name='projects'),
    path('statistics/', views.statistics, name='statistics'),
    path('logstore/', views.logstore, name='logstore'),
]
