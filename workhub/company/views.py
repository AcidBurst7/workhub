from django.shortcuts import render
# from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

from django.db.models import Q, OuterRef, Exists, Case, When, IntegerField
from django.core.paginator import Paginator

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Side, Font
from datetime import datetime
from urllib.parse import unquote

from core.helpers import get_user_group, generate_numbers_list, get_status_job_order
from core.models import Projects, ProjectStatus, Users, Company, CompanyProjects, StatusJob
from company.forms import SearchCommentsForm
from company.helpers.company_helpers import get_company_statuses_filter, \
                                            get_company_types_filter, \
                                            lost_companies, \
                                            render_lost_companies, \
                                            get_regions_filter, \
                                            get_query_for_more_content_param, \
                                            get_inactive_regions, \
                                            get_companies_from_search, \
                                            get_action_search_forms

@login_required
def view(request, compamy_id):
    return render(request, 'company/company.html')

def render_search_form(request, user_group):
    company_statuses = get_company_statuses_filter(request, user_group)
    company_statuses_choices = [
        (str(item['company_status']), f"{item['name_status']} ({item['count']})")
        for item in company_statuses
    ]
    
    company_types = get_company_types_filter(request, user_group)
    company_types_choices = [
        (str(item['id_type']), f"{item['name_type']} ({item['count']})")
        for item in company_types
    ]

    company_projects = Projects.objects.all()
    company_project_statuses = ProjectStatus.objects.all()
    company_manager = Users.objects.filter(Q(role=0) | Q(fio = "Общий")).filter(is_active=1).all()

    search_form = SearchCommentsForm(
        request.POST or None, 
        company_status=company_statuses_choices,
        company_type=company_types_choices,
        company_project=company_projects,
        company_project_status=company_project_statuses,
        company_manager=company_manager
    )

    return search_form

"""Рендер формы поиска компаний"""
@login_required
@require_http_methods(['GET'])
def search(request):
    region_id = 0
    user_group = get_user_group(request)
    
    user_id = request.user.id if user_group == "manager" else 0
    lost_user_companies = lost_companies(region_id, user_id)
    lost_user_companies_count = len(lost_user_companies)
    lost_user_companies_line = render_lost_companies(lost_user_companies)
    search_form = render_search_form(request, user_group)

    return render(request, 'company/search_company.html', {
        "user_group": user_group,
        "search_form": search_form,
        "lost_user_companies_list": lost_user_companies_line,
        "lost_user_companies_count": lost_user_companies_count
    })

"""Рендер страницы резльтата поиска компаний"""
@login_required
@require_http_methods(['POST'])
def action_search(request):
    offset = request.GET.get('offset', 0)
    companies_only = request.GET.get('companies_only')
    companies, status_order, search_request, limit = _search_companies(request, '', False, offset)
    managers, company_statuses, projects, projects_statuses = get_action_search_forms()

    if companies_only:
        return render(request, 'company/partials/search_result.html', {'companies': companies})
    else:
        return render(request, 'company/search_result.html', {
            "companies": companies,
            "status_order": status_order,
            "managers": managers, 
            "company_statuses": company_statuses, 
            "projects": projects, 
            "projects_statuses": projects_statuses,
            "companies_ids": '',
            "search_post_data": dict(request.POST.lists()),
            }
        )

def _search_companies(request, companies_ids='', all_lines=False, offset=0):
    user_group = get_user_group(request)
    status_order = get_status_job_order(request.GET.get('status_order', 'asc'))  
    limit = request.POST.get('limit', 15)
    companies = []

    query = f"SELECT id_company, name_company, director, phone, is_primary, users.fio as manager_name, name_status as status_name " \
            f"FROM company " \
            f"INNER JOIN users ON users.id_user = company.id_manager " \
            f"INNER JOIN status_job ON company.id_status_job = status_job.id_status_job " \
            f"WHERE "

    if companies_ids is not None and len(companies) > 0:
        query += f"id_company IN ({companies_ids})" 
    elif request.method == 'POST':
        regions_list = request.POST.getlist('ch_regions[]', None)
        search_form = render_search_form(request, user_group)   
        if search_form.is_valid():
            search_form_data = search_form.cleaned_data
            chproject = search_form_data['company_project']
            chproject_status = search_form_data['company_project_status']
            more_content = search_form_data['project_more_content']
            more_content_by_info = search_form_data['project_more_content_by_info']
            more_content_by_price = search_form_data['project_more_content_by_price']

            query_buf_str = ""
            manager_sql = ""
            conditions = []

            if search_form_data['project_more_content'] != '':
                query_buf_str = get_query_for_more_content_param(more_content, more_content_by_info, more_content_by_price)
            
            if regions_list is not None and len(regions_list) > 0:
                conditions.append(f"id_region in ({','.join(regions_list)})")
            
            if search_form_data['company_type']:
                conditions.append(f"id_type in ({','.join(search_form_data['company_type'])})")

            if int(search_form_data['company_manager_name']) > 0:
                manager_sql = f"company.id_manager = {search_form_data['company_manager_name']}"
                conditions.append(manager_sql)
            
            """ НАЧАЛО Фильтры "Проект", "Статус проекта", "Содержание" """
            chproject_values = ''
            chproject_status_values = ''
            if chproject and chproject_status is None:
                chproject_values = ','.join(chproject)
                chproject_values_arr = chproject_values.split(', ')

                if len(chproject_values) > 0:
                    #  Учитываем поиск по содержанию
                    query_buf_str = get_query_for_more_content_param(more_content, more_content_by_info, more_content_by_price) if more_content else ""

                    #  Если выбран хотя бы один пункт проекта
                    sql = f"(EXISTS (SELECT company_id FROM company_projects WHERE company.id_company = company_projects.company_id AND {manager_sql} AND company_projects.project_id IN ({chproject_values}) {query_buf_str}))";
                    conditions.append(sql)
            elif chproject is None and chproject_status:
                # Если не выбран проект и выбран статус
                chproject_status_values = ','.join(chproject_status)
                chproject_status_values_arr = chproject_status_values.split(', ')

                query_buf = ""
                chproject_status_query = ""
                if len(chproject_status_values) > 0:
                    if len(chproject_status_values_arr) > 1:
                        chproject_status_query = f"company_projects.status_id IN ({chproject_status_values})"
                        chproject_status_query = f"company_projects.status_id = {chproject_status_values}"

                more_content_by_info_query = "company_projects.more LIKE '%{more_content}%'"
                more_content_by_price_query = "company_projects.year LIKE '%{more_content}%'"
                if len(chproject_status_query) > 0 and more_content_by_info and more_content_by_price:
                    query_buf = f"AND {chproject_status_query} AND ({more_content_by_info_query} OR {more_content_by_price_query})"
                elif len(chproject_status_query) == 0 and more_content_by_info and more_content_by_price:
                    query_buf = f" AND ({more_content_by_info_query} OR {more_content_by_price_query})"
                elif len(chproject_status_query) > 0 and more_content_by_info is None and more_content_by_price:
                    query_buf = f" AND {chproject_status_query} AND {more_content_by_price_query}"
                elif len(chproject_status_query) > 0 and more_content_by_info and more_content_by_price is None:
                    query_buf = f" AND {chproject_status_query} AND {more_content_by_info_query}"
                elif len(chproject_status_query) == 0 and more_content_by_info is None and more_content_by_price:
                    query_buf = f" AND {more_content_by_price_query}"
                elif len(chproject_status_query) > 0 and more_content_by_info is  None and more_content_by_price is None:
                    query_buf = f" AND {chproject_status_query}"

                conditions.append(f"(EXISTS (SELECT status_id FROM company_projects WHERE company.id_company = company_projects.company_id {query_buf} AND {manager_sql} ))")
            elif chproject is None and chproject_status is None:
                # Если не выбран проект и не выбран статус, то ничего не добавляем в заброс
                if more_content:
                    query_buf_str = get_query_for_more_content_param(more_content, more_content_by_info, more_content_by_price)
                    conditions.append(f"(EXISTS (SELECT company_id FROM company_projects WHERE company.id_company = company_projects.company_id {query_buf_str} {manager_sql}))")
            elif chproject and chproject_status:
                # Если выбран проект и выбран статус
                if '0' in chproject_status:
                    query_buf_str = get_query_for_more_content_param(more_content, more_content_by_info, more_content_by_price)
                    projects_list = ','.join(chproject)

                    sql = f" (NOT EXISTS (SELECT project_id FROM company_projects WHERE company.id_company = company_projects.company_id AND company_projects.project_id IN ({projects_list}) AND {manager_sql} ))";

                    # добавляем поиск по содержанию
                    if len(query_buf_str) > 0: 
                        sql += f" AND (EXISTS (SELECT project_id FROM company_projects WHERE company.id_company = company_projects.company_id {query_buf_str} AND company_projects.project_id NOT IN ({projects_list}) ))";
                    conditions.append(sql)
                else:
                    query_buf = []
                    for chproject_line in chproject:
                        for chproject_status_line in chproject_status:
                            query_buf.append(f"(company_projects.project_id = {chproject_line}" \
                                            f" AND company_projects.status_id = {chproject_status_line})")
                    query_buf_str = f"({(' OR '.join(query_buf))})";

                    if more_content:
                        query_buf_str += get_query_for_more_content_param(more_content, more_content_by_info, more_content_by_price)

                    conditions.append(f"(EXISTS (SELECT project_id, status_id FROM company_projects WHERE company.id_company = company_projects.company_id AND {manager_sql} {query_buf_str}))")
            """ КОНЕЦ Фильтры "Проект", "Статус проекта", "Содержание" """

            if search_form_data['company_status']:
                conditions.append(f"company.id_status_job IN ({','.join(search_form_data['company_status'])})")
            
            if search_form_data['identificator_company'] != '' and int(search_form_data['identificator_company']) > 0:
                conditions.append(f"company.id_company = {search_form_data['identificator_company']}")

            if search_form_data['name_company']:
                conditions.append(f"company.name_company LIKE '%{search_form_data['name_company']}%'")

            if search_form_data['is_primary']:
                conditions.append(f"company.is_primary = {search_form_data['is_primary']}")

            if search_form_data['educational_municipal_status_id']:
                conditions.append(f"educational_municipal_status_id = {search_form_data['educational_municipal_status_id']}")

            referrer_page_arr = request.META['HTTP_REFERER'].split('/')
            if referrer_page_arr[len(referrer_page_arr) - 1] != 'statistics.php' and user_group == 'director':
                inactive_regions = get_inactive_regions()
                get_inactive_regions_list = ', '.join(inactive_regions)
                conditions.append(f'company.id_region NOT IN ({get_inactive_regions_list})')
            
            limit = search_form_data['limit']
            
            where = ' AND '.join(conditions) if len(conditions) > 0 else '1 = 1'
            query += f"{where}"

    query += f" ORDER BY status_job.order ASC "
    
    if all_lines is False:
        query += f"LIMIT {offset}, {limit}"
    
    print(query)
    companies = get_companies_from_search(query)
    
    return [companies, status_order, request, limit]
            
@login_required
def search_result(request):
    companies_ids = request.GET.get('companies_list', '')
    companies, status_order, request, limit = _search_companies(request, companies_ids)
    managers, company_statuses, projects, projects_statuses = get_action_search_forms()

    return render(request, 'company/search_result.html', {
        "companies": companies,
        "status_order": status_order,
        "managers": managers, 
        "company_statuses": company_statuses, 
        "projects": projects, 
        "projects_statuses": projects_statuses,
        "companies_ids": companies_ids
    })

def process_mass_actions(request):
    if request.method == 'POST':
        print(request.POST)

@login_required
def create(request):
    return render(request, 'company/create_company.html')

@login_required
def update(request, company_id):
    return render(request, 'company/update_company.html')

@login_required
def action_region_filter(request):
    regions_list = []
    selected_regions = []
    user_group = get_user_group(request)

    try:
        selected_regions = request.session['regions_poisk_selected']
    except KeyError:
        pass

    session_action = request.GET.get('session_action') if request.GET.get('session_action') else ""
    region_to_session = request.GET.get('region_to_session') if request.GET.get('region_to_session') else ""
    delete_session = request.GET.get('delete_session') if request.GET.get('delete_session') else ""
    query = request.GET.get('q') if request.GET.get('q') else ""
    region_name_sort = request.GET.get('region_name_sort') if request.GET.get('region_name_sort') else ""
    region_timezone_sort = request.GET.get('region_timezone_sort') if request.GET.get('region_timezone_sort') else ""

    if len(delete_session) > 0:
        if request.session.get("delete_session"):
            del request.session[delete_session]
    elif len(session_action) > 0 and len(region_to_session) > 0:
        if session_action == 'add':
            if request.session.get('regions_poisk_selected', None) is None:    
                request.session.update({'regions_poisk_selected': [region_to_session]})
            else:
                regions = request.session['regions_poisk_selected']
                if region_to_session not in regions:
                    regions.append(region_to_session)
                request.session.update({'regions_poisk_selected': regions})
        elif session_action == 'delete':
            if region_to_session == 'all':
                if request.session.get('regions_poisk_selected', None) is None:
                    del request.session['regions_poisk_selected']
            else:
                regions = request.session['regions_poisk_selected']
                if region_to_session in regions:
                    regions.remove(region_to_session)
                request.session.update({'regions_poisk_selected': regions})
    else:
        regions_list = get_regions_filter(request, 
                                          user_group, 
                                          query, 
                                          region_timezone_sort, 
                                          region_name_sort, 
                                          selected_regions)

    return JsonResponse({'status': 'ok', 'regions_list': regions_list, 'selected_regions': selected_regions})

def save_companies_to_excel(request):
    if request.method == 'POST':
        companies_ids = request.POST.get('company')
        companies, status_order, request, limit = _search_companies(request, companies_ids, True, 0)

        wb = Workbook()
        ws = wb.active
        ws.title = "Компании"

        ws.column_dimensions['A'].width = 50
        ws.column_dimensions['B'].width = 50
        ws.column_dimensions['C'].width = 50
        ws.column_dimensions['D'].width = 100

        headers = ['Название компании', 'Директор', 'Телефон', 'Ссылка']
        ws.append(headers)

        header_style = {
            'font': Font(bold=True, name='Arial'),
            'alignment': Alignment(horizontal='center', vertical='center', wrap_text=True),
            'border': Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )
        }

        for col in 'ABCD':
            cell = ws[f'{col}1']
            for attr, value in header_style.items():
                setattr(cell, attr, value)

        if companies:
            for i, company in enumerate(companies, start=2):
                ws[f'A{i}'] = str(company["name_company"])
                ws[f'B{i}'] = str(company["director"])
                ws[f'C{i}'] = str(company["phone"])
                link = f"http://{request.get_host()}/company/view?company_id={company["id_company"]}"
                ws[f'D{i}'] = link

                # Стили строк
                for col in 'ABCD':
                    cell = ws[f'{col}{i}']
                    cell.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
                    cell.border = Border(
                        left=Side(style='thin'),
                        right=Side(style='thin'),
                        top=Side(style='thin'),
                        bottom=Side(style='thin')
                    )
        else:
            ws['A2'] = 'Нет данных'

        # Отправляем файл
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = f"report-companies_{datetime.now().date()}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        wb.save(response)
        return response
    return HttpResponse('')

    