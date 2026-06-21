from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('download/', views.download_application_form, name='download_form'),
    path('download/file/<int:pk>/', views.serve_form_file, name='serve_form_file'),
    path('submit/', views.submit_application, name='submit'),
    path('status/', views.application_status, name='status'),
    path('detail/<int:pk>/', views.application_detail, name='detail'),
]