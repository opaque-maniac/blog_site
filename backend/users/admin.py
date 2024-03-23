from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ['email', 'first_name', 'last_name']

# Register models here
admin.site.register(CustomUser, CustomUserAdmin)
