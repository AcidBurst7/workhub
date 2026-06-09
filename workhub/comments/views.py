from django.shortcuts import render
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from core.models import Comments, RequestComments
from .forms import SearchCommentsForm, SearchCommentsInRequestsForm

@login_required
@require_http_methods(['POST', 'GET'])
def search_comments_only(request):
    comments_list = Comments.objects.all().select_related("company")
    page = request.GET.get('page')
    comments_only = request.GET.get('comments_only')
    limit = request.POST.get('limit', 15)

    search_form, comments_list, limit = _load_search_comments(request, limit)
    comments_paginator = Paginator(comments_list, limit)
    
    try:
        comments = comments_paginator.page(page)
    except EmptyPage:
        if comments_only:
            return HttpResponse('')
    except PageNotAnInteger:
        comments = comments_paginator.page(1)

    if comments_only:
        return render(request, 'comments/pages/partials/search_comments.html', {'comments': comments})
    else:
        return render(request, 'comments/pages/search_comments.html', {'comments': comments, "search_form": search_form})

@login_required
@require_http_methods(['POST', 'GET'])
def search_comments(request):    
    page = request.GET.get('page')
    comments_only = request.GET.get('comments_only')
    limit = request.GET.get('page', 15)

    search_form, comments_list, limit = _load_search_comments(request, limit)
    comments_list_count = comments_list.count()
    comments_paginator = Paginator(comments_list, limit)
    page_number = 1 if request.method == 'POST' else request.GET.get('page', 1)

    try:
        comments = comments_paginator.page(page_number)
    except EmptyPage:
        comments = comments_paginator.page(comments_paginator.num_pages)
    except PageNotAnInteger:
        comments = comments_paginator.page(1)

    return render(request, 
            'comments/pages/search_comments.html', 
            {
                'comments': comments,
                "search_form": search_form,
                "comments_list_count": comments_list_count,
                "comments_list_count2": comments_paginator.object_list.count()
            }
        )

@login_required
def _load_search_comments(request, limit):
    comments_list = Comments.objects.all().select_related("company")

    if request.method == 'POST':
        search_form = SearchCommentsForm(request.POST)
        if search_form.is_valid():
            form_data = search_form.cleaned_data

            if form_data['date_comment_from'] is not None:
                comments_list = comments_list.filter(date_comment__gte=form_data['date_comment_from'])

            if form_data['date_comment_to'] is not None:
                comments_list = comments_list.filter(date_comment__lte=form_data['date_comment_to'])

            if form_data['name_company'] is not None and form_data['name_company'] != '':
                comments_list = comments_list.filter(company__name_company__contains=form_data['name_company'])

            if form_data['status_job'] is not None and form_data['status_job'] != '0':
                comments_list = comments_list.filter(company__status_job=int(form_data['status_job']))

            if form_data['comment_result'] is not None and form_data['comment_result'] != "-1":
                comments_list = comments_list.filter(result=form_data['comment_result'])

            if form_data['text_comment'] is not None and form_data['text_comment'] != '':
                comments_list = comments_list.filter(comment__contains=form_data['text_comment'])

            if form_data['users'] is not None and form_data['users'] != '0':
                comments_list = comments_list.filter(id_user=int(form_data['users']))

            if form_data['limit'] is not None:
                limit = int(form_data['limit'])
    else:
        search_form = SearchCommentsForm()

    comments_list = comments_list.order_by('-date_comment')
    return [search_form, comments_list, limit]

@login_required
def search_comments_in_requests(request):
    search_form, comments_list, limit = _load_search_comments_in_requests(request)
    comments_list_count = comments_list.count()
    comments_paginator = Paginator(comments_list, limit)
    page_number = 1 if request.method == 'POST' else request.GET.get('page', 1)

    try:
        comments = comments_paginator.page(page_number)
    except EmptyPage:
        comments = comments_paginator.page(comments_paginator.num_pages)
    except PageNotAnInteger:
        comments = comments_paginator.page(1)
    
    return render(request, 'comments/pages/search_comments_in_requests.html', 
                  {
                    "comments": comments,
                    "search_form": search_form,
                    "comments_list_count": comments_list_count,
                    "comments_list_count2": comments_paginator.object_list.count()
                  })

@login_required
def _load_search_comments_in_requests(request):
    comments_list = RequestComments.objects.select_related("request", "request__company")
    limit = 15

    if request.method == 'POST':
        search_form = SearchCommentsInRequestsForm(request.POST)
        if search_form.is_valid():
            form_data = search_form.cleaned_data

            if form_data['date_comment_from'] is not None:
                comments_list = comments_list.filter(created_at__gte=form_data['date_comment_from'])

            if form_data['date_comment_to'] is not None:
                comments_list = comments_list.filter(created_at__lte=form_data['date_comment_to'])

            if form_data['users'] is not None and form_data['users'] != '0':
                comments_list = comments_list.filter(user_id=int(form_data['users']))
    else:
        search_form = SearchCommentsInRequestsForm()

    comments_list = comments_list.only(
        "request_id", "text", "created_at", "status",  # поля RequestComments
        "request__id", # поля Request
        "request__company__company", "request__company__name_company"  # поля Company
    ).order_by('-created_at')
    return [search_form, comments_list, limit]

@login_required
@require_http_methods(['POST', 'GET'])
def search_comments_in_requests_only(request):
    page = request.GET.get('page')
    comments_in_requests_only = request.GET.get('comments_in_requests_only')

    search_form, comments_list, limit = _load_search_comments_in_requests(request)
    comments_paginator = Paginator(comments_list, limit)
    
    try:
        comments = comments_paginator.page(page)
    except EmptyPage:
        if comments_in_requests_only:
            return HttpResponse('')
    except PageNotAnInteger:
        comments = comments_paginator.page(1)

    if comments_in_requests_only:
        return render(request, 'comments/pages/partials/search_comments_in_requests.html', {'comments': comments})
    else:
        return render(request, 'comments/pages/search_comments_in_requests.html', {'comments': comments, "search_form": search_form})

