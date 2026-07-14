import csv
from django.http import HttpResponse
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


@login_required
def export_applications_csv(request):
    if not request.user.is_admin:
        return redirect('home')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tuk_bursary_applications_report.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Application Ref', 'Student Name', 'Student Email', 'Student Admission Number',
        'Course', 'Year of Study', 'Vulnerability Details', 'Family Background',
        'Amount Requested (KES)', 'Status', 'Reviewed By', 'Reviewed At', 'Feedback to Student'
    ])

    applications = Application.objects.select_related('student', 'student__studentprofile', 'reviewed_by').all()

    for app in applications:
        profile = getattr(app.student, 'studentprofile', None)
        adm_no = profile.student_number if profile else ''
        course = profile.course if profile else ''
        year = profile.get_year_of_study_display() if profile else ''
        reviewer = app.reviewed_by.full_name if app.reviewed_by else ''
        reviewed_at = app.reviewed_at.strftime('%Y-%m-%d %H:%M') if app.reviewed_at else ''

        writer.writerow([
            app.pk,
            app.student.full_name,
            app.student.email,
            adm_no,
            course,
            year,
            app.vulnerability_details,
            app.family_background,
            app.amount_requested or 0,
            app.get_status_display(),
            reviewer,
            reviewed_at,
            app.feedback_to_student
        ])

    return response


@login_required
def export_payments_csv(request):
    if not request.user.is_admin:
        return redirect('home')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tuk_bursary_payments_report.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Receipt Ref', 'Student Name', 'Student Email', 'Student Admission Number',
        'Application Ref', 'Amount Deposited (KES)', 'Issuing Office / Bank',
        'Date Uploaded', 'Verification Status'
    ])

    payments = Payment.objects.select_related('student', 'student__studentprofile', 'application').all()

    for payment in payments:
        profile = getattr(payment.student, 'studentprofile', None)
        adm_no = profile.student_number if profile else ''
        app_ref = f"Ref #{payment.application.pk}" if payment.application else ''
        status = 'Verified' if payment.verified else 'Pending Verification'
        uploaded_at = payment.uploaded_at.strftime('%Y-%m-%d %H:%M')

        writer.writerow([
            payment.pk,
            payment.student.full_name,
            payment.student.email,
            adm_no,
            app_ref,
            payment.amount,
            payment.bank_name or '',
            uploaded_at,
            status
        ])

    return response