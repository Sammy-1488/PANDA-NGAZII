from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .models import User, StudentProfile


TUK_STUDENT_DOMAIN = getattr(settings, 'TUK_STUDENT_EMAIL_DOMAIN', 'students.tuk.ac.ke')


class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label='First Name')
    last_name = forms.CharField(max_length=100, label='Last Name')
    email = forms.EmailField(
        label='TUK Student Email',
        help_text=f'Must be your official TUK email (e.g. s123456@{TUK_STUDENT_DOMAIN})',
    )
    phone = forms.CharField(max_length=15, required=False, label='Phone Number')
    student_number = forms.CharField(max_length=20, label='Student Admission Number')
    course = forms.CharField(max_length=200, label='Course / Programme')
    year_of_study = forms.ChoiceField(
        choices=StudentProfile.YEAR_CHOICES,
        label='Year of Study',
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if not email.endswith(f'@{TUK_STUDENT_DOMAIN}'):
            raise forms.ValidationError(
                f'Only TUK student emails are accepted (@{TUK_STUDENT_DOMAIN}).'
            )
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean_student_number(self):
        sn = self.cleaned_data['student_number'].strip().upper()
        if StudentProfile.objects.filter(student_number=sn).exists():
            raise forms.ValidationError('This student number is already registered.')
        return sn

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data.get('phone', '')
        user.is_student = True
        # Auto-generate username from email (before the @)
        base_username = self.cleaned_data['email'].split('@')[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        user.username = username
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                student_number=self.cleaned_data['student_number'],
                course=self.cleaned_data.get('course', ''),
                year_of_study=self.cleaned_data.get('year_of_study', 1),
            )
        return user


TUK_STAFF_DOMAIN = getattr(settings, 'TUK_STAFF_EMAIL_DOMAIN', 'tuk.ac.ke')


class AdminRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label='First Name')
    last_name = forms.CharField(max_length=100, label='Last Name')
    email = forms.EmailField(
        label='TUK Staff/Admin Email',
        help_text=f'Must be your official TUK staff email (e.g. name@{TUK_STAFF_DOMAIN})',
    )
    phone = forms.CharField(max_length=15, required=False, label='Phone Number')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if not email.endswith(f'@{TUK_STAFF_DOMAIN}'):
            raise forms.ValidationError(
                f'Only TUK staff/admin emails are accepted (@{TUK_STAFF_DOMAIN}).'
            )
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data.get('phone', '')
        user.is_admin = True
        user.is_staff = True
        # Auto-generate username from email (before the @)
        base_username = self.cleaned_data['email'].split('@')[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        user.username = username
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='TUK Email Address',
        widget=forms.EmailInput(attrs={'placeholder': 'your.email@tuk.ac.ke', 'autofocus': True}),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}),
    )


class StudentProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = StudentProfile
        fields = ('course', 'year_of_study')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['phone'].initial = self.user.phone

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.phone = self.cleaned_data.get('phone', '')
            if commit:
                self.user.save()
        if commit:
            profile.save()
        return profile