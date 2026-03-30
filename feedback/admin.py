from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('student', 'qualification_status', 'reviewed_by', 'reviewed_at')
    list_filter = ('qualification_status', 'reviewed_at')