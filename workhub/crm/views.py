from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

# from .models import Reminders, TasksPom, StatusJob, Company, Comments, Users
from core.models import Reminders, TasksPom, Tasks, StatusJob, Company, Comments, Users, RequestComments
from account.models import Profile
from .forms import SearchCommentsForm, SearchCommentsInRequestsForm

@login_required
def index(request):
    tasks_count = 0
    tasks_pom_count = 0
    important_tasks_count = 0
    reminders_count = 0
    
    user_group = 'guest'
    for group in request.user.groups.all():
        user_group = group.name
    
    if user_group == 'guest':
        return redirect('account:logout')
    
    user_profile = Profile.objects.get(user_id=request.user.id)

    if user_group in ['manager', 'director'] or user_profile is not None:
        old_user_id = user_profile.old_user_id
        
        if user_group == 'manager':
            tasks_pom_count = TasksPom.objects.filter(id_user_ruk=old_user_id)
            tasks_count = Tasks.objects.filter(id_user_isp=old_user_id).\
                                        exclude(check_task='on').\
                                        all().count()
            important_tasks_count = Tasks.objects.filter(id_user_isp=old_user_id).\
                                            filter(id_user_ruk=24).\
                                            exclude(check_task='on').\
                                            all().count() 
        elif user_group == 'director':
            tasks_pom_count = TasksPom.objects.filter(id_user_isp=old_user_id)
                                     
        tasks_pom_count = tasks_pom_count.filter(date_task_end__isnull=True). \
                                order_by('date_task_end', 'date_task','id_task'). \
                                all().count() 
        reminders_count = Reminders.objects.filter(id_user=old_user_id).\
                                exclude(check_reminder='on').\
                                all().count()
        tasks_divide = 0
        if tasks_count > 0 and important_tasks_count > 0 and tasks_count != important_tasks_count:
            tasks_divide = important_tasks_count / tasks_count
    
    return render(request, 'crm/pages/index.html', {
        'reminders_count': reminders_count, 
        'tasks_pom_count': tasks_pom_count,
        'tasks_count': tasks_count,
        'tasks_divide': tasks_divide,
        'important_tasks_count': important_tasks_count,
        'user_group': user_group,
    })

@login_required
def search_reminders(request):
    return render(request, 'crm/search_reminders.html')

@login_required
def tasks(request):
    return render(request, 'crm/tasks.html')

@login_required
def requests(request):
    return render(request, 'crm/requests.html')

@login_required
def search_request(request):
    return render(request, 'crm/search_request.html')

@login_required
def tasks_pom(request):
    return render(request, 'crm/tasks_pom.html')

@login_required
def projects(request):
    return render(request, 'crm/projects.html')

@login_required
def statistics(request):
    return render(request, 'crm/statistics.html')

@login_required
def logstore(request):
    return render(request, 'crm/logstore.html')

@login_required
def calendar(request):
    return render(request, 'crm/calendar.html')