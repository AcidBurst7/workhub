from django import forms
from django.contrib.auth.models import User, Group

from core.models import StatusJob, Users, Regions

class SearchRemindersForm(forms.Form):
    blank_choice = [(0, 'Не имеет значения'),] 
    company_status_choices = StatusJob.objects.all().order_by('order')
    users_choices = Users.objects.all().order_by('fio')
    regions_choices = Regions.objects.all().order_by('name_region')
    limits = {15: 15, 50: 50, 100: 100, 150: 150, 200: 200}
    main_card_choices = {"": 'Не имеет значения', 0: "Нет", 1: "Да"}
    
    date_reminder_from = forms.DateField(
        label="Начальная дата:",
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"},),
    )
    date_reminder_to = forms.DateField(
        label="Конечная дата:",
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"},),
    )
    regions = forms.TypedChoiceField(
        empty_value=0,
        label="Регион:",
        required=False,
        choices=[],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    name_company = forms.CharField(
        label="Наименование компании:",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    status_job = forms.TypedChoiceField(
        empty_value=0,
        label="Рабочий статус:",
        required=False,
        choices=[],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    reminder_keyword = forms.CharField(
        empty_value="",
        label="Ключевое слово в напоминании:",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    users = forms.TypedChoiceField(
        empty_value=0,
        label="ФИО пользователя:",
        required=False,
        choices=[],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    limit = forms.TypedChoiceField(
        empty_value=15,
        label="Количество записей:",
        required=False,
        choices=limits,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    main_card = forms.TypedChoiceField(
        empty_value="",
        label="Главная карточка:",
        required=False,
        choices=main_card_choices,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        blank_choice = [('', '---------')]

        self.fields['status_job'].choices = (
            blank_choice +
            [
                (obj.pk, obj.name_status)
                for obj in self.company_status_choices
            ]
        )

        self.fields['users'].choices = (
            blank_choice +
            [
                (obj.pk, obj.fio)
                for obj in self.users_choices
            ]
        )

        self.fields['regions'].choices = (
            blank_choice +
            [
                (obj.pk, obj.name_region)
                for obj in self.regions_choices
            ]
        )

class SearchRemindersByRequestsForm(forms.Form):
    blank_choice = [(0, 'Не имеет значения'),] 
    company_status_choices = StatusJob.objects.all()
    users_choices = Users.objects.filter(id_user__in=[67, 89, 88, 87]).all().order_by('fio')
    regions_choices = Regions.objects.all().order_by('name_region')

    date_from = forms.DateField(
        label="Начальная дата:",
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"},),
    )
    date_to = forms.DateField(
        label="Конечная дата:",
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"},),
    )
    regions = forms.TypedChoiceField(
        empty_value=0,
        label="Регион:",
        required=False,
        choices=[],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    name_company = forms.CharField(
        label="Наименование компании:",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    director = forms.CharField(
        empty_value="",
        label="Директор:",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    status_job = forms.TypedChoiceField(
        empty_value=0,
        label="Рабочий статус:",
        required=False,
        choices=[],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    users = forms.TypedChoiceField(
        empty_value=67,
        label="ФИО пользователя:",
        required=False,
        choices=[],
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        blank_choice = [('', '---------')]

        self.fields['status_job'].choices = (
            blank_choice +
            [
                (obj.pk, obj.name_status)
                for obj in self.company_status_choices
            ]
        )

        self.fields['users'].choices = (
            blank_choice +
            [
                (obj.pk, obj.fio)
                for obj in self.users_choices
            ]
        )

        self.fields['regions'].choices = (
            blank_choice +
            [
                (obj.pk, obj.name_region)
                for obj in self.regions_choices
            ]
        )
