from rest_framework import viewsets
from students.models import Student
from payments.models import Payment
from transactions.models import Transactions
from .serializers import StudentSerializer, PaymentSerializer, TransactionSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class TransactionLogViewSet(viewsets.ModelViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer