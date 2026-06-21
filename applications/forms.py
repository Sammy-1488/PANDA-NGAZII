from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'vulnerability_details',
            'family_background',
            'amount_requested',
            'supporting_documents',
            'filled_form',
        ]
        widgets = {
            'vulnerability_details': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Describe your financial situation, any challenges you face paying fees...',
            }),
            'family_background': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Briefly describe your family background (number of dependants, parents/guardians employment status, etc.)...',
            }),
            'amount_requested': forms.NumberInput(attrs={
                'placeholder': 'e.g. 35000',
                'min': '0',
            }),
        }
        labels = {
            'vulnerability_details': 'Financial Vulnerability Statement',
            'family_background': 'Family Background',
            'amount_requested': 'Amount Requested (KES)',
            'supporting_documents': 'Supporting Documents',
            'filled_form': 'Completed Application Form (PDF/Word)',
        }
        help_texts = {
            'amount_requested': 'Enter the total amount you are requesting in Kenyan Shillings.',
            'supporting_documents': 'Upload a single file (PDF/ZIP) containing: national ID, fee statement, school letter, guardian details.',
            'filled_form': 'Download the blank form from the portal, fill it in, then upload it here.',
        }


class ApplicationReviewForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'feedback_to_student', 'admin_notes']
        widgets = {
            'feedback_to_student': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'This message will be displayed to the student...',
            }),
            'admin_notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Internal notes (not visible to student)...',
            }),
        }
        labels = {
            'status': 'Application Status',
            'feedback_to_student': 'Message to Student',
            'admin_notes': 'Internal Admin Notes',
        }