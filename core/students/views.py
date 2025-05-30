from django.shortcuts import render
from .models import Student
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def student_dashboard(request):
    student_dashboard = Student.objects.get(id=request.user.id)
    context = {
        'student': student_dashboard,
    }
    return render(request, 'students/student_dashboard.html', context)

@login_required
def student_profile(request):
    student = Student.objects.get(id=request.user.id)
    context = {
        'student': student,
    }
    return render(request, 'students/student_profile.html', context)

# create grading app
@login_required
def student_grades(request):
    student = Student.objects.get(id=request.user.id)
    grades = student.grades.all()
    context = {
        'student': student,
        'grades': grades,
    }
    return render(request, 'students/student_grades.html', context)

@login_required
def student_attendance(request):
    student = Student.objects.get(id=request.user.id)
    attendance_records = student.attendance_records.all()
    context = {
        'student': student,
        'attendance_records': attendance_records,
    }
    return render(request, 'students/student_attendance.html', context)