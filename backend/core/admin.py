from django.contrib import admin
from .models import Complaints

class ComplaintAdmin(admin.ModelAdmin):
    search_fields = ['email', 'name', 'phone']
    
# Register your models here.
admin.site.register(Complaints, ComplaintAdmin)