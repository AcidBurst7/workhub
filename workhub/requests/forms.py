from django import forms
from .fields import GroupedModelChoiceField

from core.models import Users, RequestStatuses, RequestReminders

class UpdateRequestStatusForm(forms.Form):
    request_statuses_choices = RequestStatuses.objects.all()
    
    request_status = forms.TypedChoiceField(
        label="",
        required=True,
        choices=[],
        widget=forms.Select(attrs={"class": "form-select"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['request_status'].choices = [
            (obj.pk, obj.name)
            for obj in request_statuses_choices
        ]

class UpdateRequestUserForm(forms.Form):
    blank_choice = [(0, 'Не назначен'),] 
    tech_users_choices = Users.objects.filter(role__in=[2, 3], is_active=1).all()
    
    request_user = forms.TypedChoiceField(
        label="",
        required=True,
        choices=[],
        widget=forms.Select(attrs={"class": "form-select"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        blank_choice = [('', '---------')]

        self.fields['request_user'].choices = (
            blank_choice +
            [
                (obj.pk, obj.fio)
                for obj in tech_users_choices
            ]
        )

class UpdateRequestsForm(forms.Form):
    blank_choice = [(0, 'Не назначена'),] 
    request_statuses_choices = RequestStatuses.objects.filter(closed__lt=2).all().order_by('closed')
    tech_users_choices = Users.objects.filter(role__in=[2, 3], is_active=1).all()

    title = forms.CharField(
        label="Наименование заявки:",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    status_id = forms.TypedChoiceField(
        label="Статус:",
        required=True,
        choices=[],
        widget=forms.Select(attrs={"class": "form-select"})
    )
    user_id = forms.TypedChoiceField(
        label="Специалист:",
        required=True,
        choices=[],
        widget=forms.Select(attrs={"class": "form-select"})
    )
    company_name = forms.CharField(
        label="Наименование компании:",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    company_type = forms.CharField(
        label="Тип компании:",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": True})
    )
    company_region = forms.CharField(
        label="Регион:",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": True})
    )
    company_district = forms.CharField(
        label="Район:",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "readonly": True})
    )
    company_address = forms.CharField(
        label="Адрес:",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    company_phone = forms.CharField(
        label="Телефон:",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    company_email = forms.CharField(
        label="Электронная почта:",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    company_director = forms.CharField(
        label="Директор:",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    company_contact = forms.CharField(
        label="Другое контактное лицо, должность, телефон:",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    contract_name = forms.CharField(
        label="Номер/наименование договора (копируем из договора):",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    contract_subject = forms.CharField(
        label="Предмет договора (копируем из договора):",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    contract_start = forms.DateField(
        label="Дата начала работ:",
        required=True,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"},),
    )
    contract_time = forms.CharField(
        label="Срок работы (копируем из договора):",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    contract_terms = forms.CharField(
        label="Условия согласования (копируем из договора):",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    contract_agreement = forms.CharField(
        label="Устная договоренность:",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    contract_population = forms.CharField(
        label="Численность населения / часовой пояс:",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    contract_owner = forms.CharField(
        label="На кого заключен договор:",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    road_length = forms.CharField(
        label="Протяженность дорог:",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    contract_info = forms.CharField(
        label="Примечание (таблицы, ТЗ измененное):",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        blank_choice = [('', '---------')]

        self.fields['status_id'].choices = [
            (choice.pk, choice.name)
            for choice in request_statuses_choices
        ]
        self.fields['user_id'].choices = (
            blank_choice +
            [
                (choice.pk, choice.fio)
                for choice in tech_users_choices
            ]
        )


class UpdateRequestReminderForm(forms.Form):
    due_date = forms.DateField(
        label="Срок:",
        required=True,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"},),
    )
    text = forms.CharField(
        label="Текст:",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )

class UpdateRequestCommentForm(forms.Form):
    request_statuses_choices = RequestStatuses.objects.filter(closed__lt=2).all().order_by('closed')

    text = forms.CharField(
        label="Текст",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    request_new_status_id = forms.TypedChoiceField(
        label="Новый статус",
        required=True,
        choices=[],
        widget=forms.Select(attrs={"class": "form-select"})
    )
    request_reminder_status = forms.BooleanField(
        label="Результативный",
        required=False
    )
    selected_reminder_due_date = forms.DateField(
        label="",
        disabled=False,
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date", "id": "reminder_due_date"},),
    )
    selected_reminder_text = forms.CharField(
        label="",
        disabled=False,
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5, "id": "reminder_text"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        blank_choice = [('', '---------')]

        self.fields['request_new_status_id'].choices = [
            (choice.pk, choice.name)
            for choice in request_statuses_choices
        ]
