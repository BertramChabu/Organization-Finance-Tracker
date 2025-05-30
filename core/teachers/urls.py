from django.urls import path
from .views import (
    ClassListView,
    AssignmentListView,
    TimetableView,
    SubmissionListView,
    TeacherLogoutView
)

urlpatterns = [
    path('classes/', ClassListView.as_view(), name='class_list'),
    path('classes/<int:class_id>/assignments/', AssignmentListView.as_view(), name='assignment_list'),
    path('timetable/', TimetableView.as_view(), name='teacher_timetable'),
    path('assignments/<int:assignment_id>/submissions/', SubmissionListView.as_view(), name='submission_list'),
    
]
