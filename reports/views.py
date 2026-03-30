from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from applications.models import Application
from payments.models import Payment
from feedback.models import Feedback

@login_required
def dashboard(request):
    if not request.user.is_admin:
        return redirect('home')
    
    total_applications = Application.objects.count()
    approved_applications = Application.objects.filter(status='approved').count()
    total_payments = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
    qualified_students = Feedback.objects.filter(qualification_status='qualified').count()
    
    context = {
        'total_applications': total_applications,
        'approved_applications': approved_applications,
        'total_payments': total_payments,
        'qualified_students': qualified_students,
    }
    return render(request, 'reports/dashboard.html', context)