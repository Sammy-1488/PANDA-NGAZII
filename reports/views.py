from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from applications.models import Application
from payments.models import Payment
from accounts.models import User


@login_required
def dashboard(request):
    if not request.user.is_admin:
        return redirect('home')

    # Application stats
    total_applications = Application.objects.count()
    pending_count = Application.objects.filter(status='pending').count()
    qualified_count = Application.objects.filter(status='qualified').count()
    approved_count = Application.objects.filter(status='approved').count()
    disbursed_count = Application.objects.filter(status='disbursed').count()
    rejected_count = Application.objects.filter(status='rejected').count()

    # Financial stats
    total_requested = Application.objects.aggregate(
        total=Sum('amount_requested')
    )['total'] or 0

    total_disbursed_payments = Payment.objects.filter(verified=True).aggregate(
        total=Sum('amount')
    )['total'] or 0

    unverified_receipts = Payment.objects.filter(verified=False).count()

    # Student stats
    total_students = User.objects.filter(is_student=True).count()

    # Recent applications (last 10)
    recent_applications = Application.objects.select_related('student').order_by('-submitted_at')[:10]

    context = {
        'total_applications': total_applications,
        'pending_count': pending_count,
        'qualified_count': qualified_count,
        'approved_count': approved_count,
        'disbursed_count': disbursed_count,
        'rejected_count': rejected_count,
        'total_requested': total_requested,
        'total_disbursed_payments': total_disbursed_payments,
        'unverified_receipts': unverified_receipts,
        'total_students': total_students,
        'recent_applications': recent_applications,
    }
    return render(request, 'reports/dashboard.html', context)