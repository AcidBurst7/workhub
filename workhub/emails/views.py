from django.shortcuts import render
from .email_fetcher import fetch_emails_, fetch_email_body
from django.http import JsonResponse

from django.core.cache import cache
from core.models import Emails, EmailCompanies, EmailsQueue


def email_list_view(request):
    """Главная страница (рендерим HTML)"""
    inbox_emails = []
    return render(request, "emails/mailbox.html")

def load_more_emails(request):
    """AJAX-запрос для загрузки дополнительных писем"""
    offset = int(request.GET.get("offset", 0))
    emails = fetch_emails_(offset=offset)

    return JsonResponse({"emails": emails})
    
def load_email_body(request):
    """AJAX-запрос для загрузки тела письма"""
    message_id = request.GET.get("uid")
    response = fetch_email_body(message_id)
    status_code = 200

    if "error" in response:
        status_code = response["code"]

    return JsonResponse(response=response, status_code=status_code)