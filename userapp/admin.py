from django.contrib import admin

from userapp.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tg_username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'tg_id')
