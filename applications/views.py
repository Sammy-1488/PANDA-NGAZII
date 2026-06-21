from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse
from django.utils import timezone
from .forms import ApplicationForm, ApplicationReviewForm
from .models import Application, ApplicationFormTemplate


STATUS_ORDER = ['pending', 'qualified', 'approved', 'disbursed']


def _enrich(applications):
    enriched = []
    for app in applications:
        step_index = STATUS_ORDER.index(app.status) if app.status in STATUS_ORDER else -1
        enriched.append({
            'app': app,
            'step_index': step_index,
            'is_rejected': app.status == 'rejected',
            'is_disbursed': app.status == 'disbursed',
        })
    return enriched


@login_required
def download_application_form(request):
    """Serve the latest active application form template for download."""
    template = ApplicationFormTemplate.objects.filter(is_active=True).first()
    return render(request, 'applications/download_form.html', {'form_template': template})


@login_required
def serve_form_file(request, pk):
    """Stream the actual form file to the browser as a download."""
    template = get_object_or_404(ApplicationFormTemplate, pk=pk, is_active=True)
    response = FileResponse(template.form_file.open('rb'), as_attachment=True)
    filename = template.form_file.name.split('/')[-1]
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def submit_application(request):
    if not request.user.is_student:
        messages.error(request, 'Only registered students can submit applications.')
        return redirect('home')

    existing = Application.objects.filter(student=request.user).first()

    # Block re-submission if not pending
    if existing and existing.status not in ('pending',):
        messages.warning(
            request,
            f'Your application is currently <strong>{existing.get_status_display()}</strong> and cannot be edited. '
            'Please contact the Bursary Office if you need to make changes.'
        )
        return redirect('applications:status')

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, instance=existing)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.save()
            messages.success(
                request,
                '✅ Your application has been submitted successfully! '
                'You will be notified of any updates.'
            )
            return redirect('applications:status')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ApplicationForm(instance=existing)

    template = ApplicationFormTemplate.objects.filter(is_active=True).first()
    return render(request, 'applications/submit.html', {
        'form': form,
        'form_template': template,
        'existing': existing,
    })


@login_required
def application_status(request):
    if request.user.is_student:
        applications = Application.objects.filter(student=request.user).order_by('-submitted_at')
    elif request.user.is_admin:
        # Admins see all; support filtering
        status_filter = request.GET.get('status', '')
        applications = Application.objects.select_related('student').order_by('-submitted_at')
        if status_filter:
            applications = applications.filter(status=status_filter)
    else:
        return redirect('home')

    enriched = _enrich(applications)
    return render(request, 'applications/status.html', {
        'enriched_applications': enriched,
        'status_steps': STATUS_ORDER,
        'status_filter': request.GET.get('status', ''),
        'status_choices': Application.STATUS_CHOICES,
    })


@login_required
def application_detail(request, pk):
    """Admin: full detail view of a single application."""
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('home')

    application = get_object_or_404(Application, pk=pk)

    if request.method == 'POST':
        form = ApplicationReviewForm(request.POST, instance=application)
        if form.is_valid():
            reviewed = form.save(commit=False)
            reviewed.reviewed_by = request.user
            reviewed.reviewed_at = timezone.now()
            reviewed.save()
            messages.success(
                request,
                f'Application #{pk} updated to <strong>{reviewed.get_status_display()}</strong>.'
            )
            return redirect('applications:detail', pk=pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ApplicationReviewForm(instance=application)

    return render(request, 'applications/detail.html', {
        'application': application,
        'form': form,
        'step_index': STATUS_ORDER.index(application.status) if application.status in STATUS_ORDER else -1,
        'status_steps': STATUS_ORDER,
    })