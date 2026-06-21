from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.models import User
from applications.models import Application
from .models import Feedback
from .forms import FeedbackForm


@login_required
def view_feedback(request):
    """Students see all feedback addressed to them."""
    if not request.user.is_student:
        return redirect('home')
    feedbacks = Feedback.objects.filter(student=request.user).order_by('-reviewed_at')
    # Mark all as read
    feedbacks.filter(is_read=False).update(is_read=True)
    return render(request, 'feedback/view.html', {'feedbacks': feedbacks})


@login_required
def provide_feedback(request, application_id):
    """Admin: provide feedback on a specific application."""
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('home')

    application = get_object_or_404(Application, pk=application_id)
    student = application.student

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.student = student
            feedback.application = application
            feedback.reviewed_by = request.user
            feedback.save()
            messages.success(request, f'Feedback sent to {student.full_name}.')
            return redirect('applications:detail', pk=application_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FeedbackForm()

    return render(request, 'feedback/provide.html', {
        'form': form,
        'student': student,
        'application': application,
    })


@login_required
def feedback_list(request):
    """Admin sees all feedback; students see their own."""
    if request.user.is_admin:
        feedbacks = Feedback.objects.select_related('student', 'application', 'reviewed_by').order_by('-reviewed_at')
    else:
        feedbacks = Feedback.objects.filter(student=request.user).order_by('-reviewed_at')
        feedbacks.filter(is_read=False).update(is_read=True)
    return render(request, 'feedback/list.html', {'feedbacks': feedbacks})