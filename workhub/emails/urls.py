from django.urls import path
from .views import email_list_view, load_more_emails, load_email_body

app_name = 'emails'

urlpatterns = [
    path("email_list/", email_list_view, name="email_list"),
    path("load-more-emails/", load_more_emails, name="load_more_emails"), 
    path("load-email-body/", load_email_body, name="load_email_body"), 
]