from django.urls import path
from .views import view_request,\
                    update_request, \
                    post_update_request, \
                    delete_request, \
                    update_request_status, \
                    update_request_user, \
                    update_request_reminder, \
                    update_request_reminder, \
                    delete_request_reminder, \
                    update_request_comment, \
                    delete_request_comment

app_name = 'requests'

urlpatterns = [
    path('view/<int:request_id>', view_request, name='view_request'),
    path('update/<int:request_id>', update_request, name='update_request'),
    path('post_update/<int:request_id>', post_update_request, name='post_update_request'),
    path('delete_request/<int:request_id>', delete_request, name='delete_request'),

    path('update_status/<int:request_id>', update_request_status, name='update_request_status'),
    path('update_user/<int:request_id>', update_request_user, name='update_request_user'),
    
    path('update_request_reminder/<int:request_id>/<int:request_reminder_id>', update_request_reminder, name='update_request_reminder'),
    path('delete_request_reminder/<int:request_id>/<int:request_reminder_id>', delete_request_reminder, name='delete_request_reminder'),

    path('update_request_comment/<int:request_id>/<int:request_comment_id>', update_request_comment, name='update_request_comment'),
    path('delete_request_comment/<int:request_id>/<int:request_comment_id>', delete_request_comment, name='delete_request_comment'),
]