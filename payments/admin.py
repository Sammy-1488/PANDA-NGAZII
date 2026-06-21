from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'application', 'amount', 'bank_name', 'uploaded_at', 'verified')
    list_filter = ('verified', 'uploaded_at')
    list_editable = ('verified',)
    search_fields = ('student__email', 'student__first_name', 'bank_name')
    readonly_fields = ('uploaded_at',)