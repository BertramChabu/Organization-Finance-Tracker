from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import TeacherAttendanceForm
from .models import TeacherAttendance

def is_deputy(user):
    return user.is_authenticated and user.role == 'deputy'

@login_required
@user_passes_test(is_deputy)
def record_attendance(request):
    if request.method == 'POST':
        form = TeacherAttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.recorded_by = request.user
            attendance.save()
            return redirect('attendance_list')
    else:
        form = TeacherAttendanceForm()
    return render(request, 'attendance/record_attendance.html', {'form': form})

@login_required
@user_passes_test(is_deputy)
def attendance_list(request):
    records = TeacherAttendance.objects.all().order_by('-date')
    return render(request, 'attendance/attendance_list.html', {'records': records})
