from django.contrib import admin
from .models import Profile
from core.models import Users


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'phone']
    raw_id_fields = ['user']


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id_user', 'fio', 'role', 'login', 'is_active', 'last_login']
