from django.shortcuts import render, redirect
import datetime
from core.models import Requests, RequestReminders, RequestComments, RequestStatuses, Users
from account.models import Profile
from .forms import UpdateRequestStatusForm, UpdateRequestUserForm, UpdateRequestsForm, UpdateRequestReminderForm, UpdateRequestCommentForm

def view_request(request, request_id):
    request_ = Requests.objects.filter(id=request_id).select_related("company", "user", "status").first()
    request_reminders = RequestReminders.objects.filter(request_id=request_id).order_by("-due_date").all()
    request_comments = RequestComments.objects.filter(request_id=request_id).order_by("-created_at").all()
    
    update_request_status_form = UpdateRequestStatusForm(initial={'request_status': request_.status_id})
    update_request_user_form = UpdateRequestUserForm(initial={'request_user': request_.user_id})

    return render(request, 'requests/pages/view_request.html', {
        "request_": request_,
        "request_reminders": request_reminders,
        "request_comments": request_comments,
        "update_request_status_form": update_request_status_form,
        "update_request_user_form": update_request_user_form
    })

def update_request_status(request, request_id):
    if request.method == 'POST':
        update_request_status_form = UpdateRequestStatusForm(request.POST)
        if update_request_status_form.is_valid():
            form_data = update_request_status_form.cleaned_data
            if request.POST.get("request_id", 0) != 0:
                request_ = Requests.objects.get(id=request_id)
                request_.status_id = form_data["request_status"]
                request_.save()
    return redirect("requests:view_request", request_id=request_id)

def update_request_user(request, request_id):
    if request.method == 'POST':
        update_request_user_form = UpdateRequestUserForm(request.POST)
        if update_request_user_form.is_valid():
            form_data = update_request_user_form.cleaned_data
            if request.POST.get("request_id", 0) != 0:
                request_ = Requests.objects.get(id=request_id)
                request_.user_id = form_data["request_user"]
                request_.save()
    return redirect("requests:view_request", request_id=request_id)

def show_edit_form_request(request, request_id):
    request_ = Requests.objects.filter(id=request_id).select_related("company", "user", "status").first()

    # if ['director', 'tech_manager', 'tech_director'] in request.user.groups.all():
    request_statuses_choices = RequestStatuses.objects.filter(closed__lt=2).all().order_by('closed')
    tech_users_choices = Users.objects.filter(role__in=[2, 3], is_active=1).all()

    return render(request, 'requests/pages/update_request.html', {
        "request_": request_,
        "request_statuses_choices": request_statuses_choices,
        "tech_users_choices": tech_users_choices
    })

def update_request(request, request_id):
    request_ = Requests.objects.filter(id=request_id).select_related("company", "user", "status").first()
    user_group = 'guest'
    for group in request.user.groups.all():
        user_group = group.name

    request_form = UpdateRequestsForm()
    request_form.fields['title'].initial = request_.title
    request_form.fields['status_id'].initial = request_.status_id
    request_form.fields['user_id'].initial = request_.user_id
    request_form.fields['company_name'].initial = request_.company_name
    request_form.fields['company_address'].initial = request_.company_address
    request_form.fields['company_phone'].initial = request_.company_phone
    request_form.fields['company_email'].initial = request_.company_email
    request_form.fields['company_director'].initial = request_.company_director
    request_form.fields['company_contact'].initial = f"{request_.company_contact} {request_.company_contact_phone}"
    request_form.fields['contract_name'].initial = request_.contract_name
    request_form.fields['contract_subject'].initial = request_.contract_subject
    request_form.fields['contract_start'].initial = datetime.date.strftime(request_.contract_start, "%Y-%m-%d") 
    request_form.fields['contract_time'].initial = request_.contract_time
    request_form.fields['contract_terms'].initial = request_.contract_terms
    request_form.fields['contract_agreement'].initial = request_.contract_agreement
    request_form.fields['contract_population'].initial = request_.contract_population
    request_form.fields['contract_owner'].initial = request_.contract_owner
    request_form.fields['road_length'].initial = request_.road_length
    request_form.fields['contract_info'].initial = request_.contract_info

    return render(request, 'requests/pages/update_request.html', {
            "request_": request_,
            "user_group": user_group,
            "request_form": request_form
    })

def post_update_request(request, request_id):
    request_ = Requests.objects.filter(id=request_id).select_related("company", "user", "status").first()
    user_group = 'guest'
    for group in request.user.groups.all():
        user_group = group.name

    if request.method == 'POST':
        request_form = UpdateRequestsForm(request.POST)
        if request_form.is_valid():
            form_data = request_form.cleaned_data
            request_ = Requests.objects.get(id=request_id)

            request_.title = form_data["title"]
            request_.company_name = form_data["company_name"]
            request_.status_id = form_data["status_id"]
            request_.user_id = form_data["user_id"]
            request_.company_address = form_data["company_address"]
            request_.company_phone = form_data["company_phone"]
            request_.company_email = form_data["company_email"]
            request_.company_director = form_data["company_director"]
            request_.company_contact = form_data["company_contact"]
            request_.contract_name = form_data["contract_name"]
            request_.contract_subject = form_data["contract_subject"]
            request_.contract_start = form_data["contract_start"]
            request_.contract_time = form_data["contract_time"]
            request_.contract_terms = form_data["contract_terms"]
            request_.contract_agreement = form_data["contract_agreement"]
            request_.contract_population = form_data["contract_population"]
            request_.contract_owner = form_data["contract_owner"]
            request_.road_length = form_data["road_length"]
            request_.contract_info = form_data["contract_info"]    

            return redirect("requests:view_request", request_id=request_id)
        else:
            # print(request_form.errors)
            return render(request, 'requests/pages/update_request.html', {
                "request_": request_,
                "user_group": user_group,
                "request_form": request_form
            })
    else:
        request_form = UpdateRequestsForm(request.POST)
    
    return render(request, 'requests/pages/update_request.html', {
        "request_": request_,
        "user_group": user_group,
        "request_form": request_form
    })

def delete_request(request, request_id):
    Requests.objects.get(id=request_id).delete()
    return redirect("reminders:search_reminders_by_requests")

def update_request_reminder(request, request_id, request_reminder_id):
    user_profile = Profile.objects.filter(user_id=request.user.id).first()
    request_ = Requests.objects.get(id=request_id)
    request_reminder = None
    form = UpdateRequestReminderForm()

    if request_reminder_id == 0:
        title = "Создание напоминания для заявки"
        form.fields['due_date'].initial = datetime.datetime.now()
        form.fields['text'].initial = ""
    else:
        title = "Изменение напоминания для заявки"
        request_reminder = RequestReminders.objects.get(id=request_reminder_id)
        form.fields['due_date'].initial = request_reminder.due_date.strftime("%Y-%m-%d")
        form.fields['text'].initial = request_reminder.text

    if request.method == 'POST':
        form = UpdateRequestReminderForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if request_reminder_id == 0:
                RequestReminders.objects.create(
                    request_id=request_id,
                    user_id=user_profile.old_user_id,
                    status=0,
                    text=form_data["text"],
                    due_date=form_data["due_date"]
                )
            else:
                request_reminder.text=form_data["text"]
                request_reminder.due_date=form_data["due_date"]
                request_reminder.save()
            return redirect("requests:view_request", request_id=request_id)
    return render(request, 'requests/pages/update_request_reminder.html', {
        "request_": request_,"request_reminder": request_reminder,
        "title": title,"form": form, "request_reminder_id": request_reminder_id,
        "old_user_id": user_profile.old_user_id
    })

def delete_request_reminder(request, request_id, request_reminder_id):
    RequestReminders.objects.get(pk=request_reminder_id).delete()
    return redirect("requests:view_request", request_id=request_id)

def update_request_comment(request, request_id, request_comment_id):
    user_profile = Profile.objects.filter(user_id=request.user.id).first()
    request_ = Requests.objects.get(id=request_id)
    request_reminders = RequestReminders.objects.filter(request_id=request_id).all()
    request_comment = None
    form = UpdateRequestCommentForm()

    if request_comment_id == 0:
        title = "Создание комментария для заявки"
        form.fields['text'].initial = ""
    else:
        title = "Изменение комментария для заявки"
        request_comment = RequestComments.objects.filter(id=request_comment_id).select_related('request').first()
        form.fields['text'].initial = request_comment.text
        form.fields['request_reminder_status'].initial = request_comment.status
    
    form.fields['request_new_status_id'].initial = request_.status_id

    if request.method == 'POST':
        form = UpdateRequestCommentForm(request.POST)
        if form.is_valid():
            print("after valid:")
            print(form)
            form_data = form.cleaned_data
            if request_comment_id == 0:
                request_comment = RequestComments.objects.create(
                    request_id=request_id,
                    user_id=user_profile.old_user_id,
                    status=form_data["request_reminder_status"],
                    text=form_data["text"],
                    created_at=datetime.datetime.strptime(request.POST.get("created_at").split('.')[0], "%Y-%m-%dT%H:%M:%S")
                )
            else:
                request_comment.text=form_data["text"]
                request_comment.status=form_data["request_reminder_status"]
                request_comment.created_at=datetime.datetime.strptime(request.POST.get("created_at"), "%Y-%m-%dT%H:%M:%S")
                request_comment.save()


            reminder_id = request.POST.get("reminder[id]")
            if int(reminder_id) > 0:
                request_reminder = RequestReminders.objects.get(id=reminder_id)
                request_reminder.request_id = request_.id
                if request_reminder.user_id is not None:
                    request_reminder.user_id = request_comment.user_id
                request_reminder.due_date = form_data['selected_reminder_due_date']
                request_reminder.text = form_data['selected_reminder_text']
                request_reminder.status = form_data['request_reminder_status']
                request_reminder.save()
            elif int(reminder_id) == 0:
                RequestReminders.objects.create(
                    request_id = request_.id,
                    user_id=user_profile.old_user_id,
                    status=form_data["request_reminder_status"],
                    text=form_data['selected_reminder_text'],
                    created_at=datetime.datetime.strptime(request.POST.get("created_at").split('.')[0], "%Y-%m-%dT%H:%M:%S")
                )

            request_new_status_id = form_data['request_new_status_id']
            if request_new_status_id:
                request_.status_id = request_new_status_id
                request_.save()
            
            return redirect("requests:view_request", request_id=request_id)
        
    request_statuses_choices = RequestStatuses.objects.filter(closed__lt=2).all().order_by('closed')

    return render(request, 'requests/pages/update_request_comment.html', {
        "request_": request_,"request_comment": request_comment,
        "request_reminders": request_reminders,
        "title": title,"form": form, "request_comment_id": request_comment_id,
        "request_statuses_choices": request_statuses_choices
    })

def delete_request_comment(request, request_id, request_comment_id):
    RequestComments.objects.get(id=request_comment_id).delete()
    return redirect("requests:view_request", request_id=request_id)

