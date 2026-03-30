from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from .forms import ApplicationForm
from .models import Application, ApplicationFormTemplate


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
    response['Content-Disposition'] = f'attachment; filename="{template.form_file.name.split("/")[-1]}"'
    return response


@login_required
def submit_application(request):
    if not request.user.is_student:
        return redirect('home')

    existing = Application.objects.filter(student=request.user).first()

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, instance=existing)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.save()
            return redirect('applications:status')
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
    STATUS_ORDER = ['pending', 'qualified', 'approved', 'disbursed']

    if request.user.is_student:
        applications = Application.objects.filter(student=request.user).order_by('-submitted_at')
    else:
        applications = Application.objects.all().order_by('-submitted_at')

    enriched = []
    for app in applications:
        step_index = STATUS_ORDER.index(app.status) if app.status in STATUS_ORDER else -1
        enriched.append({
            'app': app,
            'step_index': step_index,
            'is_rejected': app.status == 'rejected',
            'is_disbursed': app.status == 'disbursed',
        })

    return render(request, 'applications/status.html', {
        'enriched_applications': enriched,
        'status_steps': STATUS_ORDER,
    })