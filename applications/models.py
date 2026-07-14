# pyrefly: ignore [missing-import]
from django.db import models
# pyrefly: ignore [missing-import]
from django.conf import settings
from accounts.models import User


class ApplicationFormTemplate(models.Model):
    """Admin uploads the blank application form here for students to download."""
    title = models.CharField(max_length=200, default='TUK Bursary Application Form')
    description = models.TextField(blank=True, default='')
    form_file = models.FileField(upload_to='form_templates/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} ({self.uploaded_at.strftime('%Y-%m-%d')})"


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('qualified', 'Qualified'),
        ('approved', 'Approved'),
        ('disbursed', 'Disbursed'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={'is_student': True},
        related_name='application_set',
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )

    # Student-provided details
    vulnerability_details = models.TextField(
        help_text='Describe your financial vulnerability or hardship situation.'
    )
    family_background = models.TextField(
        help_text='Briefly describe your family background and financial situation.'
    )
    amount_requested = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text='Amount of financial support requested (KES).'
    )

    # Uploaded documents
    supporting_documents = models.FileField(
        upload_to='applications/supporting/', blank=True, null=True,
        help_text='ID copy, fee statement, school letter, etc.'
    )
    filled_form = models.FileField(
        upload_to='applications/filled_forms/', blank=True, null=True,
        help_text='Completed application form (PDF or Word).'
    )

    # Admin review fields
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to={'is_admin': True},
        related_name='reviewed_applications',
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(
        blank=True, default='',
        help_text='Internal notes by the bursary committee (not visible to student).'
    )
    feedback_to_student = models.TextField(
        blank=True, default='',
        help_text='Message displayed to the student about their application decision.'
    )

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Application #{self.pk} by {self.student.full_name} [{self.get_status_display()}]"