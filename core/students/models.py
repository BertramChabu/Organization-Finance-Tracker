from django.db import models
from parents.models import Parent
from payments.models import Payment

# -------------------------
# Grade Model
# -------------------------
class Grade(models.Model):
    FORM_CHOICES = [(str(i), f"Form {i}") for i in range(1, 5)]
    SECTION_CHOICES = [(s, s) for s in ('W', 'B', 'G', 'R')]

    form = models.CharField(max_length=1, choices=FORM_CHOICES)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES)
    date_joined = models.DateField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_form_display()} Section {self.section}"

# -------------------------
# Student Model
# -------------------------
class Student(models.Model):
    adm_no = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='students')
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Adm No: {self.adm_no})"

# -------------------------
# Student Profile
# -------------------------
class StudentProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_profiles')

    def __str__(self):
        return f"Profile: {self.student}"

# -------------------------
# Attendance
# -------------------------
class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    attended = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student} - {self.date}: {'Present' if self.attended else 'Absent'}"

# -------------------------
# Student Messages
# -------------------------
class StudentMessage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message for {self.student} on {self.created_at.strftime('%Y-%m-%d')}"

# -------------------------
# Student Events
# -------------------------
class StudentEvent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.student} on {self.event_date}"

# -------------------------
# Student Payments
# -------------------------
class StudentPayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='student_payments')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of KES {self.payment.amount} - {self.student} on {self.date.strftime('%Y-%m-%d')}"
