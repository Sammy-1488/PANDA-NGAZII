from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PaymentForm
from .models import Payment
from applications.models import Application


@login_required
def upload_payment(request):
    if not request.user.is_student:
        return redirect('home')

    # Check if student has a disbursed application
    disbursed_app = Application.objects.filter(
        student=request.user, status='disbursed'
    ).first()

    if not disbursed_app:
        messages.warning(
            request,
            "You can only upload a bank receipt after your application has been approved "
            "and funds have been disbursed. Please check your application status."
        )
        return redirect('applications:status')

    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.student = request.user
            payment.application = disbursed_app
            payment.save()
            messages.success(request, "Your bank receipt has been uploaded successfully!")
            return redirect('payments:history')
    else:
        form = PaymentForm()

    return render(request, 'payments/upload.html', {
        'form': form,
        'disbursed_app': disbursed_app,
    })


@login_required
def payment_history(request):
    if request.user.is_student:
        payments = Payment.objects.filter(student=request.user).order_by('-uploaded_at')
    else:
        payments = Payment.objects.all().order_by('-uploaded_at')
    return render(request, 'payments/history.html', {'payments': payments})