from django.contrib import admin
from .models import Application, ApplicationFormTemplate


@admin.register(ApplicationFormTemplate)
class ApplicationFormTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'is_active')
    list_editable = ('is_active',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'submitted_at', 'status')
    list_filter = ('status', 'submitted_at')
    list_editable = ('status',)