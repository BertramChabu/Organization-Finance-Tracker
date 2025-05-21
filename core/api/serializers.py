from rest_framework import serializers
from payments.models import Payment
from students.models import Student
from transactions.models import Transactions




class StudentSerializer(serializers.Serializer):
    class Meta:
        model = Student
        fields = '__all__'

class PaymentSerializer(serializers.Serializer):
    class Meta:
        model = Payment
        fields = '__all__'

class TransactionSerializer(serializers.Serializer):
    class Meta:
        model = Transactions
        fields = '__all__'


