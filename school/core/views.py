from rest_framework import generics, permissions, status, generics, permissions, filters
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    UserSerializer, UserLoginSerializer, SchoolSerializer,AcademicYearSerializer,
    SubjectSerializer, StreamSerializer, ClassSerializer,
    TeacherSerializer, StudentSerializer, ParentSerializer,
    SubjectAllocationSerializer, ExamSerializer, ExamResultSerializer,
    AttendanceSerializer, FeeStructureSerializer, FeePaymentSerializer
)

from core.models import (
    User, AcademicYear,School,
    Subject, Stream, Class, Teacher, Student, Parent,
    SubjectAllocation, Exam, ExamResult, Attendance,
    FeeStructure, FeePayment
)


# Views 
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        return Response(
            {'error': 'Invalid Credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class SchoolListCreateView(generics.ListCreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [permissions.IsAuthenticated]

class SchoolDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [permissions.IsAuthenticated]

class AcademicYearListCreateView(generics.ListCreateAPIView):
    serializer_class = AcademicYearSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        school_id = self.kwargs['school_id']
        return AcademicYear.objects.filter(school_id=school_id)

    def perform_create(self, serializer):
        school_id = self.kwargs['school_id']
        serializer.save(school_id=school_id)



# Subject Views
class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['subject_type']
    search_fields = ['name', 'code']

class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

# Stream Views
class StreamListCreateView(generics.ListCreateAPIView):
    serializer_class = StreamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        school_id = self.kwargs['school_id']
        return Stream.objects.filter(school_id=school_id)

    def perform_create(self, serializer):
        school_id = self.kwargs['school_id']
        serializer.save(school_id=school_id)

# Class Views
class ClassListCreateView(generics.ListCreateAPIView):
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        school_id = self.kwargs['school_id']
        return Class.objects.filter(school_id=school_id)

    def perform_create(self, serializer):
        school_id = self.kwargs['school_id']
        serializer.save(school_id=school_id)

# Teacher Views
class TeacherListCreateView(generics.ListCreateAPIView):
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        school_id = self.kwargs['school_id']
        return Teacher.objects.filter(school_id=school_id)

    def perform_create(self, serializer):
        school_id = self.kwargs['school_id']
        serializer.save(school_id=school_id)

# Student Views
class StudentListCreateView(generics.ListCreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        school_id = self.kwargs['school_id']
        return Student.objects.filter(school_id=school_id)

    def perform_create(self, serializer):
        school_id = self.kwargs['school_id']
        serializer.save(school_id=school_id)

# Exam Views
class ExamListCreateView(generics.ListCreateAPIView):
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        school_id = self.kwargs['school_id']
        return Exam.objects.filter(school_id=school_id)

    def perform_create(self, serializer):
        school_id = self.kwargs['school_id']
        serializer.save(school_id=school_id)

# Attendance Views
class AttendanceListCreateView(generics.ListCreateAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        return Attendance.objects.filter(student_id=student_id)

    def perform_create(self, serializer):
        student_id = self.kwargs['student_id']
        serializer.save(student_id=student_id, recorded_by=self.request.user)

# Fee Views
class FeeStructureListCreateView(generics.ListCreateAPIView):
    serializer_class = FeeStructureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        school_id = self.kwargs['school_id']
        return FeeStructure.objects.filter(school_id=school_id)

    def perform_create(self, serializer):
        school_id = self.kwargs['school_id']
        serializer.save(school_id=school_id)

class FeePaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = FeePaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs['student_id']
        return FeePayment.objects.filter(student_id=student_id)

    def perform_create(self, serializer):
        student_id = self.kwargs['student_id']
        serializer.save(student_id=student_id, received_by=self.request.user)