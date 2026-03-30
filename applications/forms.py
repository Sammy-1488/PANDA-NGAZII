from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['vulnerability_details', 'family_background', 'supporting_documents', 'filled_form']
        widgets = {
            'vulnerability_details': forms.Textarea(attrs={'rows': 4}),
            'family_background': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'vulnerability_details': 'Vulnerability Details',
            'family_background': 'Family Background',
            'supporting_documents': 'Supporting Documents (ID, School Letter, etc.)',
            'filled_form': 'Filled Application Form (PDF/Word)',
        }