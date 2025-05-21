from django.db import models

# Create your models here.
class Student(models.Model):
    adm_no = models.CharField(max_length=20, unique=True)
    firstName = models.CharField(max_length=60, blank=False, null=False)
    lastName = models.CharField(max_length=60, blank=False, null=False)
    grade = models.CharField(max_length=10)
    parent_contact = models.CharField(max_length=20)


    def __str__(self):
        return f"{self.firstName} + {self.lastName}"
    
