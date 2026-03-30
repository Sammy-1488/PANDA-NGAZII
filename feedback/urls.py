from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('view/', views.view_feedback, name='view'),
    path('provide/<int:student_id>/', views.provide_feedback, name='provide'),
    path('list/', views.feedback_list, name='list'),
]