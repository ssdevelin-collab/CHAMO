from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.shortcuts import redirect

app_name = "accounts"
name='excluir_conta'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/cliente/', views.dashboard_cliente, name='dashboard_cliente'),
    path('dashboard/prestador/', views.dashboard_prestador, name='dashboard_prestador'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('perfil-prestador/', views.perfil_prestador, name='perfil_prestador'),
    path('excluir-conta/', views.excluir_conta, name='excluir_conta'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('perfil/', views.perfil, name='perfil'),
    path('cliente/<int:user_id>/', views.perfil_cliente, name='perfil_cliente'),
    path('logout/', views.sair, name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', sair),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
