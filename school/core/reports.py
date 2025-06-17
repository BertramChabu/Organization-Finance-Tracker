from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student, ExamResult, Attendance, FeePayment, FeeStructure
from .serializers import ExamResultSerializer, StudentSerializer
from django.db.models import Avg, Count, Sum
from datetime import datetime, timedelta
from rest_framework import permissions
class StudentReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, student_id):
        student = Student.objects.get(pk=student_id)
        
        # Academic performance
        results = ExamResult.objects.filter(student=student)
        avg_score = results.aggregate(Avg('marks'))['marks__avg'] or 0
        
        # Attendance
        attendance = Attendance.objects.filter(student=student)
        present_count = attendance.filter(status='present').count()
        attendance_rate = (present_count / attendance.count()) * 100 if attendance.count() > 0 else 0
        
        # Fee balance
        total_fee = FeeStructure.objects.filter(
            school=student.school,
            academic_year=student.school.academic_years.get(is_current=True)
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        paid_amount = FeePayment.objects.filter(student=student).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        balance = total_fee - paid_amount
        
        data = {
            'student': StudentSerializer(student).data,
            'average_score': round(avg_score, 2),
            'attendance_rate': round(attendance_rate, 2),
            'fee_balance': balance,
            'last_5_results': ExamResultSerializer(results.order_by('-exam__start_date')[:5], many=True).data
        }
        
        return Response(data)

class ClassReportView(APIView):
    # Similar implementation for class-level reports
    pass