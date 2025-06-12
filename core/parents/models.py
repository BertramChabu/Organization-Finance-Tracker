from django.db import models
from django.apps import apps

class Parent(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=255, blank=True, null=True)
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
    
    def get_children(self):
        Student = apps.get_model('students', 'Student')
        return Student.objects.filter(parent=self)


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
