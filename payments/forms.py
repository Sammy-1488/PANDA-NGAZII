from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'bank_name', 'receipt']
        labels = {
            'amount': 'Bursary Amount Credited (KES)',
            'bank_name': 'Issuing Office / Bank',
            'receipt': 'Finance Office Payment Receipt (PDF or Image)',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'e.g. 15000'}),
            'bank_name': forms.TextInput(attrs={'placeholder': 'e.g. TUK Student Finance Office, Equity Bank ...'}),
        }