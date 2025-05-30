from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment
from core.students.models import Student
from django.contrib import messages

def record_payment(request):
    if request.method == 'POST':
        adm_number = request.POST.get('adm_number')
        amount = request.POST.get('amount')
        method = request.POST.get('method')
        reference = request.POST.get('reference')
        received_by = request.user.username

        student = get_object_or_404(Student, registration_number=adm_number)
        Payment.objects.create(
            student=student,
            amount=amount,
            method=method,
            reference=reference,
            received_by=received_by
        )
        messages.success(request, "Payment recorded successfully.")
        return redirect('payments_list')
    return render(request, 'payments/record_payment.html')

def payments_list(request):
    payments = Payment.objects.select_related('student').order_by('-date')
    return render(request, 'payments/payments_list.html', {'payments': payments})
