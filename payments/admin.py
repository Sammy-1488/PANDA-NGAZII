from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'uploaded_at', 'verified')
    list_filter = ('verified', 'uploaded_at')