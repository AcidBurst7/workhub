from django.urls import path

from .views import search, \
                    action_search, \
                    search_result, \
                    process_mass_actions, \
                    view, \
                    create, \
                    update, \
                    action_region_filter, \
                    save_companies_to_excel

app_name = 'company'

urlpatterns = [
    path('search/', search, name='search'),
    path('action_search/', action_search, name='action_search'),
    path('search_result/', search_result, name='search_result'),
    # path('search_companies_only/', search_companies_only, name='search_companies_only'),
    path('process_mass_actions/', process_mass_actions, name='process_mass_actions'),
    path('view/<int:company_id>', view, name='view'),
    path('create/', create, name='create'),
    path('update/<int:company_id>', update, name='update'),
    path('action_region_filter/', action_region_filter, name='action_region_filter'),

    path('save_companies_to_excel/', save_companies_to_excel, name='save_companies_to_excel'),
]