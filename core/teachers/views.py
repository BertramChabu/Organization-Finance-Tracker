from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Class, Assignment, Submission, ClassSchedule





class ClassListView(LoginRequiredMixin, ListView):
    model = Class
    template_name = 'teacher/class_list.html'
    context_object_name = 'classes'

    def get_queryset(self):
        return Class.objects.filter(teacher=self.request.user)
class AssignmentListView(LoginRequiredMixin, ListView):
    model = Assignment
    template_name = 'teacher/assignment_list.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        class_id = self.kwargs['class_id']
        return Assignment.objects.filter(related_class__id=class_id, created_by=self.request.user)


class TimetableView(LoginRequiredMixin, ListView):
    model = ClassSchedule
    template_name = 'teacher/timetable.html'
    context_object_name = 'timetable'

    def get_queryset(self):
        return ClassSchedule.objects.filter(teacher=self.request.user).order_by('day_of_week', 'start_time')

class SubmissionListView(LoginRequiredMixin, ListView):
    model = Submission
    template_name = 'teacher/submission_list.html'
    context_object_name = 'submissions'

    def get_queryset(self):
        assignment_id = self.kwargs['assignment_id']
        return Submission.objects.filter(assignment__id=assignment_id, assignment__created_by=self.request.user)
