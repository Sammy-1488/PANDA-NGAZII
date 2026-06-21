from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('view/', views.view_feedback, name='view'),
    path('list/', views.feedback_list, name='list'),
    path('provide/<int:application_id>/', views.provide_feedback, name='provide'),
]