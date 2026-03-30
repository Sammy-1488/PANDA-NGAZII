from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('upload/', views.upload_payment, name='upload'),
    path('history/', views.payment_history, name='history'),
]