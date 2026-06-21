from django.db import models
from accounts.models import User
from applications.models import Application


class Feedback(models.Model):
    FEEDBACK_TYPE_CHOICES = [
        ('info', 'General Information'),
        ('clarification', 'Clarification Required'),
        ('approval_note', 'Approval Note'),
        ('rejection_reason', 'Rejection Reason'),
    ]

    application = models.ForeignKey(
        Application, on_delete=models.CASCADE,
        related_name='feedbacks', null=True, blank=True,
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={'is_student': True},
        related_name='feedbacks',
    )
    feedback_type = models.CharField(
        max_length=30, choices=FEEDBACK_TYPE_CHOICES, default='info'
    )
    comments = models.TextField()
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to={'is_admin': True},
        related_name='given_feedbacks',
    )
    reviewed_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-reviewed_at']

    def __str__(self):
        return f"Feedback for {self.student.full_name} [{self.get_feedback_type_display()}]"