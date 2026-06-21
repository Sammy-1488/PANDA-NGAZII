from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('student', 'application', 'feedback_type', 'reviewed_by', 'reviewed_at', 'is_read')
    list_filter = ('feedback_type', 'is_read', 'reviewed_at')
    search_fields = ('student__email', 'student__first_name', 'comments')
    readonly_fields = ('reviewed_at',)