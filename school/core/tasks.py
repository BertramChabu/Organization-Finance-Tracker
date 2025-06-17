from celery import shared_task
from django.utils import timezone
from core.models import Student, FeePayment, FeeStructure
from .models import Notification
from django.core.mail import send_mail

@shared_task
def send_fee_reminders():
    # Get current active fee structures
    fee_structures = FeeStructure.objects.filter(is_active=True)
    
    for structure in fee_structures:
        # Find students who haven't paid
        paid_students = FeePayment.objects.filter(
            fee_structure=structure
        ).values_list('student_id', flat=True)
        
        unpaid_students = Student.objects.filter(
            school=structure.school
        ).exclude(id__in=paid_students)
        
        for student in unpaid_students:
            # Create notification
            Notification.objects.create(
                user=student.user,
                notification_type='fee',
                title='Fee Payment Reminder',
                message=f'Kindly pay {structure.name} fee of {structure.amount}',
                related_url='/fees'
            )
            
            # Send email if available
            if student.user.email:
                send_mail(
                    'Fee Payment Reminder',
                    f'Dear {student.user.first_name},\n\nKindly pay {structure.name} fee of {structure.amount}',
                    'noreply@schoolsystem.com',
                    [student.user.email],
                    fail_silently=True,
                )
    
    return f"Sent reminders to {unpaid_students.count()} students"