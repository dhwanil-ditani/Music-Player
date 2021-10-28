from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_artist', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_artist')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('is_staff', 'is_artist', 'is_superuser', 'is_active', 'groups')

admin.site.register(User, UserAdminConfig)
