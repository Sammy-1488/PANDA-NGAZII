from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('submit/', views.submit_application, name='submit'),
    path('status/', views.application_status, name='status'),
    path('download-form/', views.download_application_form, name='download_form'),
    path('download-form/<int:pk>/file/', views.serve_form_file, name='serve_form_file'),
]