from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES =[
        ('bursar', 'Bursar'),
        ('principal', 'Principal'),
        ('admin', 'Admin'),
        ('parent', 'Parent'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),

    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,  null=True, blank=True)