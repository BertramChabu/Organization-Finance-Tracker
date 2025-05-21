from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.shortcuts import render
from payments.models import Payment
from students.models import Student
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import calendar
from datetime import datetime
from django.views.decorators.csrf import csrf_protect

from django.shortcuts import render


def teacher_dashboard(request):
    return render(request, 'dashboard/teacher_dashboard.html')


@csrf_protect
def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # redirect based on role
            if role == 'bursar':
                return redirect('bursar_dashboard')
            elif role == 'teacher':
                return redirect('teacher_dashboard')
            ...
        else:
            error = "Invalid credentials"
    return render(request, 'users/login.html', {'error': error})  # use `request`

class RegisterView(generics.CreateAPIView):
    queryset =  User.objects.all()
    serializer_class =  RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        return data
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


def logout_view(request):
    logout(request)
    return redirect('login_page')





def finance_view(request):
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
    return render(request, 'dashboard/finance_dashboard.html', context)
