from django.contrib import admin
from .models import Application, ApplicationFormTemplate


@admin.register(ApplicationFormTemplate)
class ApplicationFormTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('title',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'student', 'amount_requested', 'submitted_at', 'status', 'reviewed_by', 'reviewed_at')
    list_filter = ('status', 'submitted_at')
    list_editable = ('status',)
    search_fields = ('student__email', 'student__first_name', 'student__last_name')
    readonly_fields = ('submitted_at', 'updated_at', 'reviewed_at')
    fieldsets = (
        ('Student Info', {'fields': ('student', 'submitted_at', 'updated_at')}),
        ('Application Content', {'fields': ('vulnerability_details', 'family_background', 'amount_requested', 'filled_form', 'supporting_documents')}),
        ('Review', {'fields': ('status', 'reviewed_by', 'reviewed_at', 'feedback_to_student', 'admin_notes')}),
    )