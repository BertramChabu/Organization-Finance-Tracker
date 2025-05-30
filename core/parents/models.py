from django.db import models
from students.models import Student
class Parent(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=255, blank=True, null=True)
    students = models.ManyToManyField(Student, related_name='parents')
    id_number = models.CharField(max_length=20, unique=True)  # Use CharField for IDs
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    relationship = models.CharField(
        max_length=20,
        choices=[
            ('father', 'Father'),
            ('mother', 'Mother'),
            ('guardian', 'Guardian'),
            ('other', 'Other'),
        ],
        default='guardian'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.relationship})"
class FeeBalance(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.student} - Balance: {self.amount_due}"

class Message(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message to {self.parent} on {self.created_at.strftime('%Y-%m-%d')}"

class PlannedEvent(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateField()
    parents = models.ManyToManyField(Parent, related_name='events')

    def __str__(self):
        return self.title
