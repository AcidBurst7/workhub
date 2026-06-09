from django import forms

from core.models import StatusJob, Users

class SearchCommentsForm(forms.Form):
    blank_choice = [(0, 'Не имеет значения'),]
    comment_results = {-1: "Не имеет значения", 0: "Н", 1: "Р"}
    limits = {15: 15, 50: 50, 100: 100, 150: 150, 200: 200}

    date_comment_from = forms.DateField(
        label="Дата переговоров от:",
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"},),
    )
    date_comment_to = forms.DateField(
        label="Дата переговоров до:",
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"},),
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
    comment_result = forms.TypedChoiceField(
        label="Результат звонка:",
        empty_value=-1,
        choices=comment_results,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    text_comment = forms.CharField(
        empty_value="",
        label="Ключевое слово в комментарии:",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    users =  forms.TypedChoiceField(
        empty_value=0,
        label="Пользователь:",
        required=False,
        choices=[],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    limit = forms.TypedChoiceField(
        empty_value=15,
        label="Количество записей::",
        required=False,
        choices=limits,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        blank_choice = [('', '---------')]

        self.fields['status_job'].choices = (
            blank_choice +
            [
                (obj.pk, obj.name_status)
                for obj in StatusJob.objects.all()
            ]
        )

        self.fields['users'].choices = (
            blank_choice +
            [
                (obj.pk, obj.fio)
                for obj in Users.objects.all().order_by('fio')
            ]
        )

class SearchCommentsInRequestsForm(forms.Form):
    blank_choice = [(0, 'Не имеет значения'),] 
    users_choices = Users.objects.filter(id_user__in=[67, 89, 88, 87]).all().order_by('fio')

    date_comment_from = forms.DateField(
        label="Дата переговоров от:",
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"},),
    )
    date_comment_to = forms.DateField(
        label="Дата переговоров до:",
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"},),
    )
    users =  forms.TypedChoiceField(
        empty_value=0,
        label="Пользователь:",
        required=False,
        choices=[],
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        blank_choice = [('', '---------')]

        self.fields['users'].choices = (
            blank_choice +
            [
                (obj.pk, obj.fio)
                for obj in users_choices
            ]
        )
