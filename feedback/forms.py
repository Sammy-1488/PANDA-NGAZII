from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['qualification_status', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4}),
        }