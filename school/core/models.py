from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


class User(AbstractUser):
    USER_TYPES = [
        ('admin', 'System Admin'),
        ('principal', 'Principal'),
        ('teacher', 'Teacher'),
        ('student', 'student'),
        ('parent', 'Parent'),
        ('clerk', 'School Clerk'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    phone_number = models.CharField(max_length=15, blank=True)
    national_id = models.CharField(max_length=20, blank=True, unique=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Add these to resolve the conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="core_user_groups",
        related_query_name="core_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="core_user_permissions",
        related_query_name="core_user",
    )

    def __str__(self):
        return self.username

class School(models.Model):
    SCHOOL_TYPES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('church', 'Church'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    school_type = models.CharField(max_length=20, choices=SCHOOL_TYPES)
    county = models.CharField(max_length=50)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    principal = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='school_principal')
    established_year = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class AcademicYear(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='academic_years')
    year = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        unique_together = ['school', 'year']

    def __str__(self):
        return f"{self.school.name} - {self.year}"

    

class Term(models.Model):
    TERM_CHOICES = [
        (1, 'TERM 1'),
        (2, 'TERM 2'),
        (3, 'TERM 3'),
    ]
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='terms')
    term_number = models.PositiveIntegerField(choices=TERM_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        unique_together = ['academic_year', 'term_number']

    def __str__(self):
        return f"{self.academic_year.school.name} - {self.academic_year.year} Term {self.term_number}"
    
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

# Add these below your existing models

class Subject(models.Model):
    SUBJECT_TYPES = [
        ('compulsory', 'Compulsory'),
        ('optional', 'Optional'),
        ('technical', 'Technical'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    subject_type = models.CharField(max_length=20, choices=SUBJECT_TYPES)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Stream(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)  # e.g., "North", "South", "Red", "Blue"
    capacity = models.PositiveIntegerField()

    class Meta:
        unique_together = ['school', 'name']

    def __str__(self):
        return f"{self.school.name} - {self.name}"

class Class(models.Model):
    FORM_CHOICES = [
        (1, 'Form 1'),
        (2, 'Form 2'),
        (3, 'Form 3'),
        (4, 'Form 4'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    form = models.PositiveIntegerField(choices=FORM_CHOICES)
    class_teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ['school', 'stream', 'form']
        verbose_name_plural = "Classes"

    def __str__(self):
        return f"{self.school.name} - Form {self.form} {self.stream.name}"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    tsc_number = models.CharField(max_length=20, blank=True)
    subjects = models.ManyToManyField(Subject)
    is_active = models.BooleanField(default=True)
    date_hired = models.DateField()

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.school.name}"

class Student(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    admission_number = models.CharField(max_length=20, unique=True)
    current_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_admission = models.DateField()
    kcpe_marks = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(500)]
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['school', 'admission_number']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.admission_number}"

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    students = models.ManyToManyField(Student)
    occupation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} (Parent)"

class SubjectAllocation(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['teacher', 'subject', 'class_obj', 'academic_year']

    def __str__(self):
        return f"{self.teacher} teaches {self.subject} to {self.class_obj}"

class Exam(models.Model):
    EXAM_TYPES = [
        ('cat', 'CAT'),
        ('midterm', 'Mid-Term'),
        ('endterm', 'End-Term'),
        ('kcse', 'KCSE Mock'),
    ]
    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.academic_year}"

class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['exam', 'student', 'subject']

    def save(self, *args, **kwargs):
        # Auto-calculate grade
        if self.marks >= 80: self.grade = 'A'
        elif self.marks >= 75: self.grade = 'A-'
        elif self.marks >= 70: self.grade = 'B+'
        elif self.marks >= 65: self.grade = 'B'
        elif self.marks >= 60: self.grade = 'B-'
        elif self.marks >= 55: self.grade = 'C+'
        elif self.marks >= 50: self.grade = 'C'
        elif self.marks >= 45: self.grade = 'C-'
        elif self.marks >= 40: self.grade = 'D+'
        elif self.marks >= 35: self.grade = 'D'
        else: self.grade = 'E'
        super().save(*args, **kwargs)

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ['student', 'date']

class FeeStructure(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.academic_year}"

class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, default=1)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    receipt_number = models.CharField(max_length=50, unique=True)
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.student} - {self.receipt_number}"