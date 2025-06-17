from django.urls import path

from .views import (
    UserCreateView, UserLoginView, CurrentUserView, SchoolListCreateView, SchoolDetailView,AcademicYearListCreateView,
    SubjectListCreateView, SubjectDetailView,
    StreamListCreateView, ClassListCreateView,
    TeacherListCreateView, StudentListCreateView,
    ExamListCreateView, AttendanceListCreateView,
    FeeStructureListCreateView, FeePaymentListCreateView
)
from .reports import StudentReportView, ClassReportView
urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('schools/', SchoolListCreateView.as_view(), name='school-list'),
    path('schools/<uuid:pk>/', SchoolDetailView.as_view(), name='school-detail'),
    path('schools/<uuid:school_id>/academic-years/', 
         AcademicYearListCreateView.as_view(), 
         name='academic-year-list'),
    # Subjects
    path('subjects/', SubjectListCreateView.as_view(), name='subject-list'),
    path('subjects/<uuid:pk>/', SubjectDetailView.as_view(), name='subject-detail'),
    
    # School Structure
    path('schools/<uuid:school_id>/streams/', StreamListCreateView.as_view(), name='stream-list'),
    path('schools/<uuid:school_id>/classes/', ClassListCreateView.as_view(), name='class-list'),
    
    # People
    path('schools/<uuid:school_id>/teachers/', TeacherListCreateView.as_view(), name='teacher-list'),
    path('schools/<uuid:school_id>/students/', StudentListCreateView.as_view(), name='student-list'),
    
    # Academics
    path('schools/<uuid:school_id>/exams/', ExamListCreateView.as_view(), name='exam-list'),
    
    # Attendance
    path('students/<uuid:student_id>/attendance/', AttendanceListCreateView.as_view(), name='attendance-list'),
    
    # Finance
    path('schools/<uuid:school_id>/fee-structures/', FeeStructureListCreateView.as_view(), name='fee-structure-list'),
    path('students/<uuid:student_id>/fee-payments/', FeePaymentListCreateView.as_view(), name='fee-payment-list'),

    # Reports 
    path('students/<uuid:student_id>/report/', StudentReportView.as_view(), name='student-report'),
    path('classes/<uuid:class_id>/report/', ClassReportView.as_view(), name='class-report'),
]