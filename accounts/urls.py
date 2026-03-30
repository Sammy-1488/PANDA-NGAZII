from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Root path
    path('register/student/', views.register_student, name='register_student'),
    path('register/admin/', views.register_admin, name='register_admin'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),  # New about page
]