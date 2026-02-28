from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard-cliente/', views.dashboard_cliente, name='dashboard_cliente'),
    path('dashboard-prestador/', views.dashboard_prestador, name='dashboard_prestador'),

    path('perfil-prestador/', views.perfil_prestador, name='perfil_prestador'),
]