from django import forms

class SearchCommentsForm(forms.Form):
    attrs_textinput = {"class": "form-control"}
    attrs_checkbox = {"class": "form-check-input"}
    attrs_select = {"class": "form-select"}

    name_company = forms.CharField(
        label="", 
        required=False, 
        widget=forms.TextInput(attrs=attrs_textinput)
    )
    identificator_company = forms.CharField(
        label="", 
        required=False, 
        widget=forms.TextInput(attrs=attrs_textinput)
    )
    project_more_content = forms.CharField(
        label="", 
        required=False, 
        widget=forms.TextInput(attrs=attrs_textinput)
    )
    project_more_content_by_info = forms.BooleanField(
        label="", 
        required=False, 
        widget=forms.CheckboxInput(attrs=attrs_checkbox)
    )
    project_more_content_by_price = forms.BooleanField(
        label="", 
        required=False, 
        widget=forms.CheckboxInput(attrs=attrs_checkbox)
    )
    company_status = forms.MultipleChoiceField(
        label="", 
        required=False, 
        widget=forms.CheckboxSelectMultiple(attrs=attrs_checkbox)
    )
    company_type = forms.MultipleChoiceField(
        label="", 
        required=False, 
        widget=forms.CheckboxSelectMultiple(attrs=attrs_checkbox)
    )
    company_project = forms.MultipleChoiceField(
        label="", 
        required=False, 
        widget=forms.CheckboxSelectMultiple(attrs=attrs_checkbox)
    )
    company_project_status = forms.MultipleChoiceField(
        label="", 
        required=False, 
        widget=forms.CheckboxSelectMultiple(attrs=attrs_checkbox)
    )
    is_primary = forms.TypedChoiceField(
        label="", 
        required=False, 
        empty_value=0,
        choices={"": "-- Выберите --", 0: "Нет", 1: "Да"},
        widget=forms.Select(attrs=attrs_select)
    )
    educational_municipal_status_id = forms.TypedChoiceField(
        label="", 
        required=False, 
        empty_value=0,
        choices={0: "-- Выберите --", 1: "Район", 2: "Округ", 3: "Город", 4: "Городское поселение", 5: "Сельское поселение"},
        widget=forms.Select(attrs=attrs_select)
    )
    company_manager_name = forms.TypedChoiceField(
        label="", 
        empty_value=0, 
        required=False,
        widget=forms.Select(attrs=attrs_select)
    )
    limit = forms.TypedChoiceField(
        empty_value=15, 
        required=False, 
        choices={15: 15, 50: 50, 100: 100, 150: 150, 200: 200, 500: 500}, 
        widget=forms.Select(attrs=attrs_select)
    )

    def __init__(self, *args, **kwargs):
        company_status = kwargs.pop('company_status', [])
        company_type = kwargs.pop('company_type', [])
        company_project = kwargs.pop('company_project', [])
        company_project_status = kwargs.pop('company_project_status', [])
        company_manager = kwargs.pop('company_manager', [])

        super().__init__(*args, **kwargs)
        
        self.fields['company_status'] = forms.MultipleChoiceField(
            choices=company_status,
            widget=forms.CheckboxSelectMultiple,
            label="",
            required=False
        )
        self.fields['company_type'] = forms.MultipleChoiceField(
            choices=company_type,
            widget=forms.CheckboxSelectMultiple,
            label="",
            required=False
        )
        self.fields['company_project'] = forms.MultipleChoiceField(
            choices=[(project.id, project.name) for project in company_project],
            widget=forms.CheckboxSelectMultiple,
            label="",
            required=False
        )
        self.fields['company_project_status'] = forms.MultipleChoiceField(
            choices=[(0, 'Нет проекта'),] + [(project_status.id, project_status.name) for project_status in company_project_status],
            widget=forms.CheckboxSelectMultiple,
            label="",
            required=False
        )
        self.fields['company_manager_name'] = forms.TypedChoiceField(
            choices=[(0, 'Выберите пользователя'),] + [(manager.id_user, manager.fio) for manager in company_manager],
            widget=forms.Select(attrs=self.attrs_select),
            empty_value=0, 
            label="",
            required=False
        )
        
