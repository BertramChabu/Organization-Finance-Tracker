import csv
from django.http import HttpResponse 
from payments.models import Payment
def export_csv(request):
    method = request.GET.get('method')
    start_date= request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    

    payments= Payment.objects.all()

    if method:
        payments = payments.filter(method=method)
    if start_date:
        payments = payments.filter(timestamp__date__get=start_date)
    if end_date:
        payments = payments.filter(timestamp__date__get=end_date)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=payments.csv'


    writer = csv.writer(response)
    writer.writerow(['Student', 'Amount', 'Method', 'Date'])

    for p in payments:
        writer.writerow([p.students.firstName, p.students.lastName, p.amount, p.method, p.timestamp.strftime('%Y-%m-%d')])

    return response 
    
