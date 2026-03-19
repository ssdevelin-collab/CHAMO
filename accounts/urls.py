from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/cliente/', views.dashboard_cliente, name='dashboard_cliente'),
    path('dashboard/prestador/', views.dashboard_prestador, name='dashboard_prestador'),
    
    # PERFIS
    path('perfil/', views.perfil, name='perfil'),  # ← USA A VIEW perfil
    path('perfil-prestador/', views.perfil_prestador, name='perfil_prestador'),
    path('cliente/<int:user_id>/', views.perfil_cliente, name='perfil_cliente'),
    
    # AÇÕES
    path('excluir-conta/', views.excluir_conta, name='excluir_conta'),
    path('logout/', views.sair, name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)