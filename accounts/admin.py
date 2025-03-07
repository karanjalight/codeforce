from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *

# Register your models here.
admin.site.site_header = "CODEFORCE"
admin.site.site_title = "CODEFORCE"
admin.site.index_title = "CODEFORCE"
admin.site.welcome_sign = "Welcome to the CODEFORCE Admin Panel"


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (_('Personal info'), {'fields': ('email', 'username', 'name', 'phone_number', 'about_you')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_admin', 'is_parent', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    list_display = ('email', 'username', 'name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_admin', 'is_parent')
    search_fields = ('email', 'username', 'name', 'phone_number')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(CustomUser, UserAdmin)

