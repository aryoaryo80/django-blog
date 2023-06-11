from typing import Any, Optional
from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreateForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm

    list_display = ('username', 'email', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
         'fields': ('full_name', 'biography', 'email', 'phone_number', 'last_login', 'is_active')}),
        ('Permissions', {'fields': ('is_admin',
         'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'password1',
         'password2'), 'classes': ('wide',)}),
    )

    readonly_fields = ('last_login',)

    search_fields = ('username',)
    ordering = ('is_admin',)
    filter_horizontal = ('groups', 'user_permissions')

    def get_form(self, request, obj, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form
