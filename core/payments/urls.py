from django.urls import path
from . import views

urlpatterns = [
    path('record/', views.record_payment, name='record_payment'),
    path('list/', views.payments_list, name='payments_list'),
]