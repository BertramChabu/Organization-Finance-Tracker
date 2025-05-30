from django import forms
from .models import TeacherAttendance

class TeacherAttendanceForm(forms.ModelForm):
    class Meta:
        model = TeacherAttendance
        fields = ['class_instance', 'teacher', 'date', 'attended']
