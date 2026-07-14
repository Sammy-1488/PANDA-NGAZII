from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('export/applications/', views.export_applications_csv, name='export_applications'),
    path('export/payments/', views.export_payments_csv, name='export_payments'),
]