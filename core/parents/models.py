from django.db import models

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
