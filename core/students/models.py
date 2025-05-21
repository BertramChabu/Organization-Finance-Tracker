from django.db import models
from parents.models import Parent

class Grade(models.Model):
    FORM_LETTER_CHOICES = (
        ('W', 'W'),
        ('B', 'B'),
        ('G', 'G'),
        ('R', 'R'),
    )
    FORM_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )
    form = models.CharField(max_length=2, choices=FORM_CHOICES)
    section = models.CharField(max_length=1, choices=FORM_LETTER_CHOICES)
    date_joined = models.DateField()
    current_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Form {self.form} Section {self.section}"

class Student(models.Model):
    adm_no = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='students')
    
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
