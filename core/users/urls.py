from django.urls import path
from .views import (
    RegisterView, ProfileView, login_view, logout_view,
    CustomTokenObtainPairView, finance_view, teacher_dashboard
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Role dashboards
    path('dashboard/bursar/',finance_view, name='finance_dashboard'),
    # path('dashboard/headteacher/', headteacher_dashboard, name='headteacher_dashboard'),
    # path('dashboard/parent'),
    # path('dashboard/student'),
    path('dashboard/teacher/', teacher_dashboard, name='teacher_dashboard'),
]
