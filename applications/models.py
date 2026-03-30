from django.db import models
from accounts.models import User


class ApplicationFormTemplate(models.Model):
    """Admin uploads the blank application form here for students to download."""
    title = models.CharField(max_length=200, default='Application Form')
    form_file = models.FileField(upload_to='form_templates/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} ({self.uploaded_at.strftime('%Y-%m-%d')})"


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('qualified', 'Qualified'),
        ('approved', 'Approved'),
        ('disbursed', 'Disbursed'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={'is_student': True}
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    vulnerability_details = models.TextField()
    family_background = models.TextField()
    # Supporting documents (e.g. ID, school letter, etc.)
    supporting_documents = models.FileField(
        upload_to='applications/supporting/', blank=True, null=True
    )
    # The filled application form uploaded by the student
    filled_form = models.FileField(
        upload_to='applications/filled_forms/', blank=True, null=True
    )

    def __str__(self):
        return f"Application by {self.student.username} [{self.get_status_display()}]"