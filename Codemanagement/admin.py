from django.contrib import admin

# Register your models here.
from .models import Codemanagement

class CodemanagementAdmin(admin.ModelAdmin):
	list_display = ['created_time','ProjectName']

admin.site.register(Codemanagement,CodemanagementAdmin)
