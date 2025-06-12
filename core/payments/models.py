from django.db import models
from students.models import Student
class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('mpesa', 'Mpesa'),
        ('bank', 'Bank Transfer'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payment_records')

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    reference = models.CharField(max_length=100, blank=True, null=True, unique=True)
    received_by = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.student} - KES {self.amount} on {self.date.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-date']
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
