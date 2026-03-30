from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .models import Feedback
from .forms import FeedbackForm

@login_required
def view_feedback(request):
    if request.user.is_student:
        feedback = Feedback.objects.filter(student=request.user).first()
    else:
        feedback = None
    return render(request, 'feedback/view.html', {'feedback': feedback})

@login_required
def provide_feedback(request, student_id):
    if not request.user.is_admin:
        return redirect('home')
    
    student = get_object_or_404(User, id=student_id, is_student=True)
    feedback, created = Feedback.objects.get_or_create(student=student)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.reviewed_by = request.user
            feedback.save()
            return redirect('feedback:list')
    else:
        form = FeedbackForm(instance=feedback)
    return render(request, 'feedback/provide.html', {'form': form, 'student': student})

@login_required
def feedback_list(request):
    if request.user.is_admin:
        feedbacks = Feedback.objects.all()
    else:
        feedbacks = Feedback.objects.filter(student=request.user)
    return render(request, 'feedback/list.html', {'feedbacks': feedbacks})