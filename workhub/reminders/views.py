from django.shortcuts import render
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Value

from core.models import Reminders, RequestReminders, Requests, Users
from .forms import SearchRemindersForm, SearchRemindersByRequestsForm

partial_page_reminders_source = 'reminders/pages/partials/search_reminders.html'
page_reminders_source = 'reminders/pages/search_reminders.html'
partial_page_reminders_requests_source = 'reminders/pages/partials/search_reminders_by_requests.html'
page_reminders_requests_source = 'reminders/pages/search_reminders_by_requests.html'

@login_required
@require_http_methods(['POST', 'GET'])
def search_reminders_only(request):
    page = request.GET.get('page')
    reminders_only = request.GET.get('reminders_only')
    limit = request.POST.get('limit', 15)

    search_form, reminders_list, limit = _load_search_reminders(request, limit)
    reminders_paginator = Paginator(reminders_list, limit)
    
    try:
        reminders = reminders_paginator.page(page)
    except EmptyPage:
        if reminders_only:
            return HttpResponse('')
    except PageNotAnInteger:
        reminders = reminders_paginator.page(1)

    if reminders_only:
        return render(request, partial_page_reminders_source, {'reminders': reminders})
    else:
        return render(request, page_reminders_source, {'reminders': reminders, "search_form": search_form})

@login_required
@require_http_methods(['POST', 'GET'])
def search_reminders(request):  
    limit = request.POST.get('limit', 15)  
    search_form, reminders_list, limit = _load_search_reminders(request, limit)
    reminders_list_count = reminders_list.count()
    reminders_paginator = Paginator(reminders_list, limit)
    page_number = 1 if request.method == 'POST' else request.GET.get('page', 1)

    try:
        reminders = reminders_paginator.page(page_number)
    except EmptyPage:
        reminders = reminders_paginator.page(reminders_paginator.num_pages)
    except PageNotAnInteger:
        reminders = reminders_paginator.page(1)

    return render(request, page_reminders_source, {
                "reminders": reminders, \
                "search_form": search_form,\
                "limit": limit,\
                "reminders_list_count": reminders_list_count,\
                "reminders_list_count2": reminders_paginator.object_list.count()
            }
        )

@login_required
def _load_search_reminders(request, limit):
    reminders_list = Reminders.objects.select_related("company")
    
    if request.method == 'POST':
        search_form = SearchRemindersForm(request.POST)
        if search_form.is_valid():
            form_data = search_form.cleaned_data

            if form_data['date_reminder_from'] is not None:
                reminders_list = reminders_list.filter(date_reminder__gte=form_data['date_reminder_from'])

            if form_data['date_reminder_to'] is not None:
                reminders_list = reminders_list.filter(date_reminder__lte=form_data['date_reminder_to'])

            if form_data['regions'] is not None and form_data['regions'] != '0':
                reminders_list = reminders_list.filter(company__id_region=int(form_data['regions']))

            if form_data['name_company'] is not None and form_data['name_company'] != '':
                reminders_list = reminders_list.filter(company__name_company__icontains=form_data['name_company'])

            if form_data['status_job'] is not None and form_data['status_job'] != '0':
                reminders_list = reminders_list.filter(company__id_status_job=int(form_data['status_job']))

            if form_data['reminder_keyword'] is not None and form_data['reminder_keyword'] != '':
                reminders_list = reminders_list.filter(reminder__icontains=form_data['reminder_keyword'])

            if form_data['users'] is not None and form_data['users'] != '0':
                reminders_list = reminders_list.filter(id_user=int(form_data['users']))
            
            if form_data['main_card'] is not None and form_data['main_card'] != "":
                reminders_list = reminders_list.filter(company__is_primary=form_data['main_card'])

            if form_data['limit'] is not None:
                limit = int(form_data['limit'])
    else:
        search_form = SearchRemindersForm()
    
    if 'manager' in request.user.groups.all():
        users_choices = Users.objects.filter(id_user=request.user.id).all().order_by('fio')
    else:
        users_choices = Users.objects.filter(Q(role=0) | Q(fio="Общий")).filter(is_active=1).all()  

    search_form.fields['users'].choices = [(0, 'Не имеет значения'),] + [(choice.pk, choice.fio) for choice in users_choices]

    reminders_list = reminders_list.filter(check_reminder="").order_by('date_reminder').all()

    return [search_form, reminders_list, limit]



@login_required
def search_reminders_by_requests(request):
    limit = request.POST.get('limit', 15)
    search_form, reminders_list, limit = _load_search_reminders_by_requests(request, limit)
    reminders_list_count = reminders_list.count()
    reminders_paginator = Paginator(reminders_list, limit)
    page_number = 1 if request.method == 'POST' else request.GET.get('page', 1)

    try:
        reminders_requests = reminders_paginator.page(page_number)
    except EmptyPage:
        reminders_requests = reminders_paginator.page(reminders_paginator.num_pages)
    except PageNotAnInteger:
        reminders_requests = reminders_paginator.page(1)

    return render(request, page_reminders_requests_source, {
                    "reminders_requests": reminders_requests,
                    "search_form": search_form,
                    "reminders_list_count": reminders_list_count,
                    "reminders_list_count2": reminders_paginator.object_list.count()
                  })

@login_required
def _load_search_reminders_by_requests(request, limit):
    reminders_list = RequestReminders.objects.select_related("request", "request__company")

    if request.method == 'POST':
        search_form = SearchRemindersByRequestsForm(request.POST)
        if search_form.is_valid():
            form_data = search_form.cleaned_data

            if form_data['date_from'] is not None:
                reminders_list = reminders_list.filter(request__created_at__gte=form_data['date_from'])

            if form_data['date_to'] is not None:
                reminders_list = reminders_list.filter(request__created_at__lte=form_data['date_to'])

            if form_data['regions'] is not None and form_data['regions'] != '0':
                reminders_list = reminders_list.filter(request__company__id_region=int(form_data['regions']))

            if form_data['name_company'] is not None and form_data['name_company'] != '':
                reminders_list = reminders_list.filter(request__company__name_company__icontains=form_data['name_company'])

            if form_data['status_job'] is not None and form_data['status_job'] != '0':
                reminders_list = reminders_list.filter(request__company__id_status_job=int(form_data['status_job']))

            if form_data['director'] is not None and form_data['director'] != '':
                reminders_list = reminders_list.filter(request__company__director__icontains=form_data['director'])

            if form_data['users'] is not None and form_data['users'] != '0':
                reminders_list = reminders_list.filter(request__user_id=int(form_data['users']))
    else:
        search_form = SearchRemindersByRequestsForm()

    reminders_list = reminders_list.order_by('due_date')

    return [search_form, reminders_list, limit]

@login_required
@require_http_methods(['POST', 'GET'])
def search_reminders_by_requests_only(request):
    limit = request.POST.get('limit', 15)
    page = request.GET.get('page')
    reminders_by_requests_only = request.GET.get('reminders_by_requests_only')

    search_form, reminders_list, limit = _load_search_reminders_by_requests(request, limit)
    reminders_paginator = Paginator(reminders_list, limit)

    try:
        reminders = reminders_paginator.page(page)

    except EmptyPage:
        if reminders_by_requests_only:
            return HttpResponse('')
    except PageNotAnInteger:
        reminders = reminders_paginator.page(1)

    if reminders_by_requests_only:
        return render(request, partial_page_reminders_requests_source, {'reminders_requests': reminders})
    else:
        return render(request, page_reminders_requests_source, {'reminders_requests': reminders, "search_form": search_form})
