from django.db import models
from core.students.models import Student

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, choices=[('cash', 'Cash'), ('mpesa', 'Mpesa'), ('bank', 'Bank Transfer')])
    reference = models.CharField(max_length=100, blank=True, null=True)
    received_by = models.CharField(max_length=100)  # Bursar name or user

    def __str__(self):
        return f"{self.student} - {self.amount} on {self.date.date()}"
