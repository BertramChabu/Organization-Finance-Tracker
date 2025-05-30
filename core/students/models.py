from django.db import models
from parents.models import Parent
from payments.models import Payment
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
    
class StudentProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.student.first_name} {self.student.last_name}"

class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(auto_now_add=True)
    attended = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'date')  # Prevent duplicate entries

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.date} - {'Present' if self.attended else 'Absent'}"

class StudentMessage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message to {self.student.first_name} {self.student.last_name} on {self.created_at.strftime('%Y-%m-%d')}"
    
class StudentEvent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateField()

    def __str__(self):
        return f"Event: {self.title} for {self.student.first_name} {self.student.last_name} on {self.event_date}"

class StudentPayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='student_payments')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.payment.amount} for {self.student.first_name} {self.student.last_name} on {self.date.strftime('%Y-%m-%d')}"