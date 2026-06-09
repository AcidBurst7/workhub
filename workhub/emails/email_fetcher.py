import imaplib
import email
import datetime
from email.header import decode_header
from django.http import JsonResponse
from email.utils import parsedate_tz, mktime_tz
from email import policy
from django.conf import settings
from datetime import datetime
import pytz
import re
import base64
from django.db.models import Q
import traceback
from imap_tools import MailBox, EmailAddress 

from core.models import Company


TIMEZONE = "Europe/Moscow"  # Укажи нужный часовой пояс

def parse_email_date(date_str):
    """Парсит строку даты и возвращает datetime"""
    if not date_str:
        return None  # Если даты нет, возвращаем None
    
    try:
        email_date = email.utils.parsedate_to_datetime(date_str)
        return email_date.astimezone(pytz.timezone(TIMEZONE)) if email_date else None
    except Exception as e:
        print(f"Ошибка парсинга даты: {e}")
        return None  # В случае ошибки возвращаем None
    
def format_email_date(date_str):
    """Форматирует дату письма в нужный вид"""
    if not date_str:
        return "Неизвестно"  # Если даты нет, возвращаем заглушку
    
    try:
        email_date = email.utils.parsedate_to_datetime(date_str)
        if not email_date:
            return "Неизвестно"

        email_date = email_date.astimezone(pytz.timezone(TIMEZONE))  # Приводим к локальному времени
        now = datetime.now(pytz.timezone(TIMEZONE))

        if email_date.date() == now.date():
            return email_date.strftime("%H:%M")  # Если сегодня → "часы:минуты"
        return email_date.strftime("%d.%m.%Y %H:%M")  # Иначе → "день.месяц-год часы:минуты"
    
    except Exception as e:
        print(f"Ошибка форматирования даты: {e}")
        return "Ошибка даты"  # Заглушка при ошибке

def format_date(date_string):
    """Функция для форматирования даты в читаемый вид"""
    if date_string:
        date_tuple = parsedate_tz(date_string)
        if date_tuple:
            return f"{date_tuple[2]:02d}.{date_tuple[1]:02d}.{date_tuple[0]} {date_tuple[3]:02d}:{date_tuple[4]:02d}"
    return "(Неизвестная дата)"

def extract_email_address(sender):
    """Извлекает email отправителя из заголовка"""
    sender_name, sender_email = email.utils.parseaddr(sender)
    return sender_email  # Возвращаем только email

def decode_mime_words(mime_string):
    """Функция для декодирования MIME строк (например, для заголовков и имен файлов)."""
    decoded_string, encoding = decode_header(mime_string)[0]
    if isinstance(decoded_string, bytes):
        return decoded_string.decode(encoding or "utf-8")
    return decoded_string

def extract_attachments(msg, attachment_files=None):
    """Рекурсивная функция для извлечения вложений из письма."""
    if attachment_files is None:
        attachment_files = []
    
    # Если сообщение многокомпонентное
    if msg.is_multipart():
        # Проходим по всем частям письма
        for part in msg.walk():
            # Получаем тип содержимого и его параметры
            content_disposition = str(part.get("Content-Disposition"))
            content_type = part.get_content_type()

            # Проверка, является ли часть вложением
            if "attachment" in content_disposition or "inline" in content_disposition:
                filename = part.get_filename()
                if filename:
                    # Декодируем имя файла (если оно в кодировке)
                    decoded_filename = decode_mime_words(filename)
                    attachment_files.append(decoded_filename)
                    print("AttachmentIN:", decoded_filename)

            # Рекурсивно обрабатываем вложения внутри частей (если они есть)
            elif content_type == "multipart/alternative" or content_type == "multipart/mixed":
                extract_attachments(part, attachment_files)

    else:
        # Если письмо не многокомпонентное, проверяем на вложения
        content_disposition = str(msg.get("Content-Disposition"))
        if "attachment" in content_disposition or "inline" in content_disposition:
            filename = msg.get_filename()
            if filename:
                # Декодируем имя файла (если оно в кодировке)
                decoded_filename = decode_mime_words(filename)
                attachment_files.append(decoded_filename)
                print("Attachment:", decoded_filename)

    return attachment_files

def fetch_emails_(offset=0, limit=25):
    emails = []
    # Get date, subject and body len of all emails from INBOX folder
    with MailBox(settings.IMAP_SERVER).login(settings.EMAIL_ACCOUNT, settings.EMAIL_PASSWORD, initial_folder='INBOX') as mailbox:
        for msg in mailbox.fetch(criteria = "ALL", mark_seen = False, bulk=True, limit=slice(offset, limit+offset), headers_only=False, reverse=True):
            attachments = []

            for att in msg.attachments:  
                attachments.append(att.filename)

            current_user_id = 44
            company_info = {}
            manager_name = ""
            # .filter(id_manager=current_user_id) \
            company = Company.objects.select_related("id_manager") \
                                    .filter(Q(email__contains=msg.from_values.email) | Q(cont_pers__contains=msg.from_values.email)) \
                                    .first()
            if company is not None:
                company_info = {"id": company.company, "name": company.name_company}
                manager_name = company.id_manager.fio

            emails.append({
                "uid": msg.uid,
                "company": company_info,
                "manager": manager_name,
                "forwarded": "$Forwarded" in msg.flags,
                "flagged": "\\Flagged" in msg.flags,
                "subject": msg.subject,
                "sender_name": msg.from_values.name,  
                "sender_email": msg.from_values.email,
                "date_sent": format_email_date(msg.date_str),
                "datetime": msg.date,  # Храним raw datetime для сортировки
                "attachments": attachments
            })
    emails.sort(key=lambda x: x["datetime"], reverse=True)
    return emails

def fetch_emails(offset=0, limit=7):
    """Получает письма с заданного смещения (offset) и в количестве limit"""
    mail = imaplib.IMAP4_SSL(settings.IMAP_SERVER)
    mail.login(settings.EMAIL_ACCOUNT, settings.EMAIL_PASSWORD)
    mail.select("inbox", readonly=True)  # <<< ВАЖНО! Чтобы избежать изменения статуса писем

    result, data = mail.uid("Search", None, "ALL")
    email_uids = data[0].split()
    email_uids = email_uids[-(offset + limit): -offset] if offset else email_uids[-limit:]
    email_uids.sort(reverse=True)

    if not email_uids:
        print("Нет писем в ящике.")
        return []

    emails = []
    
    for uid in email_uids:
        try:
            uid_str = uid.decode()
            result1, header_data = mail.uid("FETCH", uid_str, "(BODY.PEEK[HEADER])")
            # result1, header_data = mail.fetch(uid, "(BODY.PEEK[HEADER] BODY.PEEK[MIME])")
            if result1 != "OK":
                print(f"Ошибка при FETCH заголовков UID {uid}: {result1}")
                continue

            raw_email = header_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Декодируем заголовки
            subject, encoding = decode_header(msg["Subject"] or "Без темы")[0]
            subject = subject.decode(encoding or "utf-8") if isinstance(subject, bytes) else subject

            sender, encoding = decode_header(msg["From"])[0]
            sender = sender.decode(encoding or "utf-8") if isinstance(sender, bytes) else sender
            sender_email = extract_email_address(msg["From"])  # Достаем чистый email

            email_date = parse_email_date(msg["Date"])  # Получаем datetime
            date = format_email_date(msg["Date"])  # Форматируем дату

            print(f"datetime:{email_date}")
            attachments = [] #extract_attachments(header_data)  # Извлекаем список файлов
            # for part in msg.walk():
            #     print(f"get_content_type={part.get_content_type()}")
            #     print(f"get_content_disposition={part.get_content_disposition()}")
            #     if part.get_content_disposition() == 'attachment':
            #         print(part.get_filename())
            #     print(f"datetime:{email_date}")
            # print("=============================================")

            # Получаем BODYSTRUCTURE и вложения
            status, body_structure = mail.uid("FETCH", uid, "(BODYSTRUCTURE)")  # Получаем структуру вложений
            if status != "OK":
                print(f"Ошибка при получении структуры для письма с UID {uid}")
                continue

            attachment_files = []  # Список для хранения имен файлов вложений
            for response_part in body_structure:
                if isinstance(response_part, bytes):
                    structure = response_part.decode(errors="ignore")
                    # Ищем вложения в структуре
                    if "attachment" in structure:
                        filename = None
                        if "filename" in structure:
                            print("filename in structure")
                            # Ищем имя файла в структуре (если оно есть)
                            filename = structure.split("\"filename\"")[1].split("\"")[1]
                            _, charset, _, text, _ = filename.split('?', maxsplit=4)
                            filename = base64.b64decode(text).decode(charset)
                            attachment_files.append(filename)
                            print("Attachment:", filename)
            # Проверка вложений, если они есть
            attachment_files = extract_attachments(msg, attachment_files)

            # Если вложений нет
            if not attachment_files:
                print("No attachments found.")
            print("=============================================")
                    
            emails.append({
                "uid": uid.decode(),
                "subject": subject,
                "sender_name": sender,  
                "sender_email": sender_email,
                "date_sent": date,
                "datetime": email_date,  # Храним raw datetime для сортировки
                "attachments": attachment_files
            })
        except Exception as e:
            exception_traceback = traceback.format_exc()
            print(exception_traceback, end="=========================================\n")

    mail.logout()

    # Сортируем письма от новых к старым
    # emails.sort(key=lambda x: x["datetime"], reverse=True)

    # Применяем offset и limit
    # emails = emails[offset: offset + limit]

    return emails

def fetch_email_body(request):
    """Возвращает тело письма по UID"""
    uid = request.GET.get("uid")
    if not uid:
        return {"error": "UID не указан", "code": 400}

    """Загружает тело конкретного письма по ID"""
    mail = imaplib.IMAP4_SSL(settings.IMAP_SERVER)
    mail.login(settings.EMAIL_ACCOUNT, settings.EMAIL_PASSWORD)
    mail.select("inbox", readonly=True)

    status, data = mail.uid("FETCH", uid, "(BODY.PEEK[])")
    if status != "OK":
        return {"error": f"Ошибка закгрузки письма {uid}", "code": 500}
    
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email, policy=policy.default)

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = part.get("Content-Disposition", "")

            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    # Декодируем тело письма в строку
                    body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="ignore")
                except Exception as e:
                    body = f"[Ошибка декодирования: {e}]"
    else:
        try:
            body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", errors="ignore")
        except Exception as e:
            body = f"[Ошибка декодирования: {e}]"

    mail.logout()

    # Конвертируем байтовые данные в строку, если это необходимо
    if isinstance(body, bytes):
        body = body.decode('utf-8', errors='ignore')

    body = body.replace("\r\n", "<br>").replace("\n", "<br>")

    # Возвращаем тело письма
    return {"uid": uid, "body": body}

