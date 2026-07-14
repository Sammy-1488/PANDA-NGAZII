from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_student, name='register_student'),
    path('register/admin/', views.register_admin, name='register_admin'),
    path('profile/', views.profile_view, name='profile'),
    path('about/', views.about, name='about'),
]