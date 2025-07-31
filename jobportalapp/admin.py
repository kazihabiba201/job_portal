# core/admin.py
from django.contrib import admin
from .models import Job, Application, User

admin.site.register(User)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'location', 'posted_by']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['job', 'applicant', 'applied_at']
