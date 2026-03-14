from django.urls import path
from . import views
 
app_name = 'avaliacoes'
 
urlpatterns = [
    path('avaliar/cliente/<int:pedido_id>/', views.avaliar_como_cliente, name='avaliar_como_cliente'),
    path('avaliar/prestador/<int:pedido_id>/', views.avaliar_como_prestador, name='avaliar_como_prestador'),
]