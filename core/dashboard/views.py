from django.shortcuts import render
from payments.models import Payment
from students.models import Student
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import calendar
from datetime import datetime


def dashboard_view(request):
    method = request.GET.get('method')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    payments = Payment.objects.all()

    if method:
        payments = payments.filter(method=method)

    if start_date:
        payments = payments.filter(timestamp__date__gte=start_date)
    if end_date:
        payments = payments.filter(timestamp__date__lte=end_date)

    total_payments = payments.aggregate(total=Sum('amount'))['total'] or 0
    student_count = Student.objects.count()
    pending_balances = 0

    monthly_payments = (
        payments
        .annotate(month=TruncMonth('timestamp'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    chart_labels = [calendar.month_abbr[p['month'].month] for p in monthly_payments]
    chart_data = [float(p['total']) for p in monthly_payments]

    context = {
        'total_payments': total_payments,
        'student_count': student_count,
        'pending_balances': pending_balances,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'filter_method': method,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'dashboard/index.html', context)
