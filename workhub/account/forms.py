from django import forms

from django.contrib.auth.models import User
from .models import Profile

# class LoginForm(forms.Form):
#     username = forms.CharField(
#         label="Ваш логин",
#         widget=forms.TextInput(attrs={"class": "uname", "data-icon": "u"})
#     )
#     password = forms.CharField(
#         label="Ваш пароль",
#         widget=forms.PasswordInput(attrs={"class": "youpasswd", "data-icon": "p"})
#     )

# class UserEditForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'is_active']

# class ProfileEditForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['full_name', 'phone']
    