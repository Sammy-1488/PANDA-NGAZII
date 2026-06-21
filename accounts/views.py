from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, LoginForm, StudentProfileUpdateForm
from .models import StudentProfile


def register_student(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='accounts.backends.EmailBackend')
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register_student.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required(login_url='login')
def home(request):
    context = {}
    if request.user.is_student:
        try:
            profile = request.user.studentprofile
            context['profile'] = profile
        except StudentProfile.DoesNotExist:
            pass
        # Latest application for quick status display
        latest_app = request.user.application_set.order_by('-submitted_at').first()
        context['latest_app'] = latest_app
    return render(request, 'accounts/home.html', context)


@login_required(login_url='login')
def profile_view(request):
    if not request.user.is_student:
        return redirect('home')
    profile = get_object_or_404(StudentProfile, user=request.user)
    if request.method == 'POST':
        form = StudentProfileUpdateForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        form = StudentProfileUpdateForm(instance=profile, user=request.user)
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})


def about(request):
    return render(request, 'accounts/about.html')