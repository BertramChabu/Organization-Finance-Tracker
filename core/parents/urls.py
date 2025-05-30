from django.urls import path
from . import views

urlpatterns = [
    path('parent/login/', views.parent_login, name='parent_login'),
    path('parent/logout/', views.parent_logout, name='parent_logout'),
    path('parent/dashboard/', views.parent_dashboard, name='parent_dashboard'),
]
