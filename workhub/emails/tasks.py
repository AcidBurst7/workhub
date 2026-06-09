# email_handler/tasks.py
from celery import shared_task
from .email_fetcher import fetch_emails

@shared_task
def fetch_emails_task():
    """Задача для получения писем через IMAP"""
    fetch_emails()
