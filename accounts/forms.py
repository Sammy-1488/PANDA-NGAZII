from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile

class StudentRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=False)
    student_number = forms.CharField(max_length=20)
    vulnerability_status = forms.CharField(widget=forms.Textarea)
    family_background = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                student_number=self.cleaned_data['student_number'],
                vulnerability_status=self.cleaned_data['vulnerability_status'],
                family_background=self.cleaned_data['family_background']
            )
        return user

class AdminRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = True
        if commit:
            user.save()
        return user