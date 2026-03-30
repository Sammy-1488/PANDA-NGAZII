from django.db import models
from accounts.models import User
from applications.models import Application


class Payment(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE,
        limit_choices_to={'is_student': True}
    )
    application = models.ForeignKey(
        Application, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='receipts'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # Bank deposit slip / receipt uploaded by student after depositing cheque
    receipt = models.FileField(upload_to='receipts/')
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Receipt by {self.student.username} - KES {self.amount}"