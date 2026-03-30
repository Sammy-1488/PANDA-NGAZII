from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'bank_name', 'receipt']
        labels = {
            'amount': 'Amount Deposited (KES)',
            'bank_name': 'Bank Name',
            'receipt': 'Bank Deposit Slip / Receipt (PDF or Image)',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'e.g. 15000'}),
            'bank_name': forms.TextInput(attrs={'placeholder': 'e.g. KCB, Equity, Cooperative ...'}),
        }