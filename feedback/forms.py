from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_type', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Write your message to the student here...',
            }),
        }
        labels = {
            'feedback_type': 'Feedback Type',
            'comments': 'Message / Comments',
        }