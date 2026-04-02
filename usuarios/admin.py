from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.unregister(User)

@admin.register(User)
class UsuarioAdmin(UserAdmin):
    list_display  = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter   = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering      = ('-date_joined',)
