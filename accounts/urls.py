from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)