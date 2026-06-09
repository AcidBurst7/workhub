from django.urls import path

from .views import tasks_pom_index, \
                    tasks_index

app_name = 'tasks'

urlpatterns = [
    path('tasks_index/', tasks_index, name='tasks_index'),
    path('tasks_pom_index/', tasks_index, name='actiontasks_index_search'),
]