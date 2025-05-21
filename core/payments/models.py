from django.db import models
from students.models import Student
from parents.models import Parent
# Create your models here.
class Payment(models.Model):
    
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method =  models.CharField(max_length=20, blank=False, null=False)
    reference = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.Student.firstName} + {self.Student.lastName} - {self.amount} via {self.method}"
    