from django.contrib import admin
from .models import *

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'subject_type')
    search_fields = ('name', 'code')

@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'capacity')
    list_filter = ('school',)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('get_form_display', 'stream', 'class_teacher')
    list_filter = ('school', 'stream', 'form')
    
    def get_form_display(self, obj):
        return f"Form {obj.form} {obj.stream.name}"
    get_form_display.short_description = 'Class'

# Register all other models similarly...
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(SubjectAllocation)
admin.site.register(Exam)
admin.site.register(ExamResult)
admin.site.register(Attendance)
admin.site.register(FeeStructure)
admin.site.register(FeePayment)