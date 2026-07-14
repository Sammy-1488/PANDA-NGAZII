from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PaymentForm
from .models import Payment
from applications.models import Application


@login_required
def upload_payment(request):
    if not request.user.is_student:
        return redirect('home')

    disbursed_app = Application.objects.filter(
        student=request.user, status='disbursed'
    ).first()

    if not disbursed_app:
        messages.warning(
            request,
            'You can only upload a school fees payment receipt after your application has been '
            'approved and funds have been disbursed. Please check your application status.'
        )
        return redirect('applications:status')

    # Check if already uploaded
    existing_receipt = Payment.objects.filter(
        student=request.user, application=disbursed_app
    ).first()

    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.student = request.user
            payment.application = disbursed_app
            payment.save()
            messages.success(request, '✅ Your fees payment receipt has been uploaded successfully!')
            return redirect('payments:history')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PaymentForm()

    return render(request, 'payments/upload.html', {
        'form': form,
        'disbursed_app': disbursed_app,
        'existing_receipt': existing_receipt,
    })


@login_required
def payment_history(request):
    if request.user.is_student:
        payments = Payment.objects.filter(student=request.user).order_by('-uploaded_at')
    else:
        payments = Payment.objects.select_related('student', 'application').order_by('-uploaded_at')
    return render(request, 'payments/history.html', {'payments': payments})


@login_required
def verify_payment(request, pk):
    """Admin: toggle payment verification status."""
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('home')
    payment = get_object_or_404(Payment, pk=pk)
    payment.verified = not payment.verified
    payment.save()
    status_str = 'verified' if payment.verified else 'unverified'
    messages.success(request, f'Receipt #{pk} marked as {status_str}.')
    return redirect('payments:history')