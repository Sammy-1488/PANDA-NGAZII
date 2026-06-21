from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True, null=True)

    @property
    def full_name(self):
        name = f"{self.first_name} {self.last_name}".strip()
        return name if name else self.email

    def __str__(self):
        return self.full_name or self.email


class StudentProfile(models.Model):
    YEAR_CHOICES = [
        (1, 'Year 1'),
        (2, 'Year 2'),
        (3, 'Year 3'),
        (4, 'Year 4'),
        (5, 'Year 5'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_number = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=200, blank=True, default='')
    year_of_study = models.IntegerField(choices=YEAR_CHOICES, default=1)
    vulnerability_status = models.TextField(blank=True, default='')
    family_background = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.user.full_name} ({self.student_number})"