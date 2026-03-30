from django.db import models
from accounts.models import User

class Feedback(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_student': True})
    qualification_status = models.CharField(max_length=20, choices=[
        ('qualified', 'Qualified'),
        ('not_qualified', 'Not Qualified'),
        ('pending_review', 'Pending Review'),
    ], default='pending_review')
    comments = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'is_admin': True}, related_name='reviews')
    reviewed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback for {self.student.username} - {self.qualification_status}"