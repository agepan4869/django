from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
    )

    list_filter = ('is_superuser', 'is_staff', 'is_active', 'groups')

    fieldsets = (
        ('基本情報', {'fields': ('username', 'password')}),
        (
            '権限情報',
            {
                'fields': (
                    'is_staff',
                    'is_superuser',
                    'is_active',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        ('日時情報', {'fields': ['last_login', 'date_joined']}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions'),
        }),
    )

    search_fields = ('username',)
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)