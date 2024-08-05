from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'is_staff',
        'is_superuser',
    )

    list_filter = ('is_superuser', 'is_staff')

    fieldsets = (
        ('基本情報', {'fields':('username', 'password')}),
        (
            '権限情報',
            {
                'fields':(
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        ('日時情報', {'fields': ['last_login']}),
    )

admin.site.register(CustomUser, CustomUserAdmin)